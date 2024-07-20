from sqlalchemy.orm import sessionmaker, DeclarativeBase, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs

from settings import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from settings.development import LOG_ORM

Base = declarative_base(cls=AsyncAttrs)


engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=LOG_ORM,
    pool_size=100,
    max_overflow=0,
)

async_session = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
