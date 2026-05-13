from fastapi import FastAPI

from app.core.config import settings
from app.api.routes_auth import router as auth_router


app = FastAPI(title=settings.app_name)
app.include_router(auth_router)
