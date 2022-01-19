import os
from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI

from src.auth import has_access
from src.log import configure_logging
from src.routes import auth_router, router

app = FastAPI(
    title="Health service",
    description="This app calculate pearson coefficient " "between two dependencies",
)
app.include_router(router, dependencies=[Depends(has_access)])
app.include_router(auth_router)

if __name__ == "__main__":
    logger = configure_logging(
        os.environ.get("LOG_FILE_PATH", default=Path(__file__).parent / "log.txt")
    )
    uvicorn.run(
        "main:app",
        host=os.environ.get("APP_HOST", default="0.0.0.0"),
        port=int(os.environ.get("APP_PORT", default="8000")),
    )
