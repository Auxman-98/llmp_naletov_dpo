import asyncio
from fastapi import FastAPI

from app.core.config import settings
from app.api.routes_auth import router as auth_router


async def main():
    app = FastAPI(title=settings.app_name)
    app.include_router(auth_router)


if __name__ == "__main__":
    asyncio.run(main())
