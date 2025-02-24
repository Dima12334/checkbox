import asyncio
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config.database import get_async_session, Base
from config.settings import DATABASE_TEST_URL
from src.main import app


pytest_plugins = ["tests.fixtures"]


async_test_engine = create_async_engine(DATABASE_TEST_URL, future=True)
async_test_session = async_sessionmaker(
    bind=async_test_engine, autocommit=False, autoflush=False, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session")
async def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables():
    async with async_test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with async_test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(loop_scope="session")
async def db_session():
    async with async_test_engine.connect() as connection:
        transaction = await connection.begin()
        async_session = async_sessionmaker(bind=connection, expire_on_commit=False)
        async with async_session() as session:
            yield session
        await transaction.rollback()


@pytest_asyncio.fixture(loop_scope="session")
async def override_get_async_session(db_session):
    async def _override_get_async_session():
        yield db_session

    app.dependency_overrides[get_async_session] = _override_get_async_session
    yield
    app.dependency_overrides.pop(get_async_session, None)


@pytest_asyncio.fixture(loop_scope="session")
async def client(override_get_async_session):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
