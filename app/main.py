from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.api import api_router
from app.core.configs import settings
from app.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": "Sistema Online", "docs": "/docs"}
