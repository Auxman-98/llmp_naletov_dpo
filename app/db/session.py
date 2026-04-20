from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings


db_path = "sqlite+aiosqlite:///" + settings.sqlite_path


engine = create_async_engine(db_path)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
