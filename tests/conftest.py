import pytest
from mcp_server.services import exchange_client

@pytest.fixture(autouse=True)
def mock_fetch_ticker(monkeypatch):
    async def fake_fetch_ticker(symbol: str):
        return {
            "symbol": symbol,
            "price": 100.0,
            "timestamp": 1234567890,
            "exchange": "mock"
        }
    monkeypatch.setattr(exchange_client, "fetch_ticker", fake_fetch_ticker)

@pytest.fixture(autouse=True)
def mock_fetch_historical(monkeypatch):
    async def fake_fetch_historical(symbol: str, interval="1h", limit=5):
        return [
            {
                "timestamp": 123,
                "open": 1,
                "high": 2,
                "low": 0.5,
                "close": 1.5,
                "volume": 10
            }
        ]
    monkeypatch.setattr(exchange_client, "fetch_historical", fake_fetch_historical)
