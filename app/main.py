from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)
app.include_router(auth_router)
app.include_router(chat_router)
