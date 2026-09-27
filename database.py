from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from models import Base
from config import settings



# 创建异步引擎

async_engine = create_async_engine(
    settings.database_url,
    echo=True,
    pool_size=10,
    max_overflow=20
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """应用启动时：创建尚不存在的数据表"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    """应用关闭时：释放数据库连接池"""
    await async_engine.dispose()

async def get_db():
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise