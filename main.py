from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db, close_db

from routers.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(
    title="邮书局 API",
    version="0.1.0",
    lifespan=lifespan
)
app.include_router(
    auth_router,
    prefix="/api/v1"
)

@app.get("/health")
async def root():
    return {
        "status": "ok",
        "app": "邮书局"
    }
