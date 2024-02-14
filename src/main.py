import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from app import create_app
import uvicorn

app_ = create_app()
if __name__ == "__main__":
    uvicorn.run(
        host="0.0.0.0",
        app="src.main:app_",
        reload=True
    )