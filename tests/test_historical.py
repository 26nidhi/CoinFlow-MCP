import pytest
from httpx import AsyncClient, ASGITransport
from mcp_server.main import app

@pytest.mark.asyncio
async def test_historical_valid():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/historical?symbol=BTC/USDT&interval=1h&limit=5")
        assert response.status_code == 200
        assert "data" in response.json()

@pytest.mark.asyncio
async def test_historical_invalid_symbol():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/historical?symbol=FAKE/TEST&interval=1h&limit=5")
        assert response.status_code == 400
