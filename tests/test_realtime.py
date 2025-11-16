import pytest
from httpx import AsyncClient, ASGITransport

from mcp_server.main import app
from mcp_server.services.cache import cache
from mcp_server.services.errors import InvalidSymbolError


@pytest.mark.asyncio
async def test_realtime_valid_symbol(monkeypatch):
    cache.store.clear()

    # mock the function used INSIDE routes.py
    async def fake_fetch_ticker(symbol: str):
        return {
            "symbol": symbol,
            "price": 123.45,
            "timestamp": 11111111,
            "exchange": "mock"
        }

    monkeypatch.setattr("mcp_server.routes.fetch_ticker", fake_fetch_ticker)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/realtime?symbol=BTC/USDT")

        assert response.status_code == 200
        json = response.json()
        assert json["data"]["exchange"] == "mock"
        assert json["data"]["price"] == 123.45


@pytest.mark.asyncio
async def test_realtime_invalid_symbol(monkeypatch):
    cache.store.clear()

    async def fake_fetch_ticker(symbol: str):
        raise InvalidSymbolError("Symbol not found")

    monkeypatch.setattr("mcp_server.routes.fetch_ticker", fake_fetch_ticker)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/realtime?symbol=BAD/PAIR")

        assert response.status_code == 400
