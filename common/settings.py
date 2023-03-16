from asyncio import current_task
from os import getenv

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL", "postgresql+asyncpg://telegramfs:password@postgres:5432/telegramfs")

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = async_scoped_session(
    sessionmaker(engine, expire_on_commit=False, class_=AsyncSession),
    scopefunc=current_task,
)
Base = declarative_base()
