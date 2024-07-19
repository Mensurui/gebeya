from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://iroia:mensur@127.0.0.1/gebeya"

async_engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(async_engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass
