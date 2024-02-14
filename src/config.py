import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from os.path import join, dirname
from dotenv import load_dotenv


class Settings:

    dotenv_path = join(dirname(__file__), '..', '.env')

    DB_HOST = None
    DB_PORT = None
    DB_USER = None
    DB_PASS = None
    DB_NAME = None
    DATABASE_URL_asyncpg = None

    @classmethod
    def reload_settings(cls):
        """Reloads the settings from the.env file. Used initially and after .env file has been changed."""
        load_dotenv(cls.dotenv_path, override=True)
        cls.DB_HOST = os.getenv("DB_HOST")
        cls.DB_PORT = os.getenv("DB_PORT")
        cls.DB_USER = os.getenv("DB_USER")
        cls.DB_PASS = os.getenv("DB_PASS")
        cls.DB_NAME = os.getenv("DB_NAME")
        cls.DATABASE_URL_asyncpg = (f"postgresql+asyncpg://{cls.DB_USER}:{cls.DB_PASS}"
                                    f"@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}")


Settings.reload_settings()


