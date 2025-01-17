from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from settings import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, LOG_ORM

Base = declarative_base()

engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=LOG_ORM,
    pool_size=100,
    max_overflow=0,
)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
