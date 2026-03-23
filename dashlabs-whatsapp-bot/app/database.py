import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.config import settings
from app.models import Base

# Ensure data directory exists
db_path = settings.DATABASE_URL.replace("sqlite+aiosqlite:///", "")
if db_path.startswith("./"):
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)

engine = create_async_engine(settings.DATABASE_URL, echo=(settings.APP_ENV == "development"))

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        yield session
