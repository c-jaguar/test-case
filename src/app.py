from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from dotenv import set_key
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from database import EngineClass
from fastapi.responses import RedirectResponse
from rq.job import Job
from redis import Redis
from rq import Queue
from orm import ORM
from worker import bgtask01, bgtask01_print


def create_app():
    """App initialization."""
    app = FastAPI(
        title="Test API",
    )

    connection = Redis(host='redis_server', port=6379)
    task_queue = Queue("task_queue", connection=connection)

    templates = Jinja2Templates(directory="templates")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "POST"]
    )

    @app.get("/")
    async def get_base_page(request: Request):
        return templates.TemplateResponse(name="index.html", request=request)

    @app.get("/json")
    async def get_json_page(request: Request):
        """Page with json editor representation of select query 'get_storage()'"""
        return templates.TemplateResponse(name="json.html", request=request)

    @app.get("/storage")
    async def get_storage():
        """Selects storages and items in them. Returns ODT to pass to json editor."""
        storage_json = await ORM.select_storage_dto()
        return storage_json

    @app.get("/db_settings")
    async def get_db_settings(request: Request):
        """Page with environment settings form."""
        return templates.TemplateResponse(name="db_settings.html", request=request)

    @app.post("/change_env")
    async def change_env(
            db_host: str = Form(),
            db_port: str = Form(),
            db_user: str = Form(),
            db_pass: str = Form(),
            db_name: str = Form()
    ):
        """Changes environment variables in.env file according to form values."""

        env_path = Path('..') / '.env'
        keys = ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASS', 'DB_NAME']
        values = [db_host, db_port, db_user, db_pass, db_name]
        for key, value in zip(keys, values):
            set_key(env_path, key, value)
        EngineClass.reload_engine()

        message = await ORM.check_connection()
        if "11001" in message["message"]:
            return {"message": "Connection failed"}
        else:
            return message

    @app.get("/calculate_weight")
    async def calculate_weight():
        """Enqueues calculation of sum weights by type and redirects to job result page."""
        job = task_queue.enqueue(bgtask01)
        return RedirectResponse(f"/calculate_weight/{job.id}")

    @app.get("/calculate_weight/{job_id}")
    async def test(request: Request, job_id: str):
        """Renders job result page."""
        job = Job.fetch(job_id, connection=connection)
        result = job.latest_result()

        if result:
            print(f"{result.return_value=}")
            return templates.TemplateResponse(name="job_result.html", request=request,
                                              context={"result": bgtask01_print(result.return_value),
                                                       "job_id": job_id})
        else:
            result = ("РАСЧЕТ В ПРОЦЕССЕ. РЕЗУЛЬТАТЫ БУДУТ ДОСТУПНЫ ПО ЭТОМУ АДРЕСУ.\n"
                      "ВРЕМЯ ХРАНЕНИЯ РЕЗУЛЬТАТОВ - 3 МИНУТЫ.\n"
                      "ОБНОВИТЕ СТРАНИЦУ ДЛЯ ПРОВЕРКИ ЗАВЕРШЕНИЯ РАБОТЫ.")
            return templates.TemplateResponse(name="job_result.html", request=request,
                                              context={"result": result.split('\n'),
                                                       "job_id": job_id})

    return app
