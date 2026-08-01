from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool


from app.shared.config.settings import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    poolclass = NullPool,
    pool_pre_ping=True,
)

TestingSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)