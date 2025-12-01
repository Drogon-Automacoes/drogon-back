from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.configs import settings
from app.db import init_db
from app.api.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": "Sistema Online", "docs": "/docs"}
