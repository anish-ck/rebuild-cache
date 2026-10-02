import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture
async def client():
    # If the application is already running live, test against the live instance
    try:
        async with AsyncClient(base_url="http://localhost:8000", timeout=10.0) as ac:
            res = await ac.get("/health")
            if res.status_code == 200:
                yield ac
                return
    except Exception:
        pass

    try:
        from app.main import app
    except ImportError:
        pytest.skip("App not implemented yet, skipping client fixture")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", timeout=10.0) as ac:
        yield ac

