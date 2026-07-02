from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./async_app.db"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker for generating async sessions
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Declarative base class for models
class Base(DeclarativeBase):
    pass

# Dependency to yield database sessions to endpoints
async def get_db():
    async with async_session_maker() as session:
        yield session