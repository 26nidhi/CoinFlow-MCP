from fastapi import APIRouter, Query, HTTPException

from mcp_server.services.cache import cache
from mcp_server.services.exchange_client import fetch_ticker, fetch_historical
from mcp_server.services.errors import InvalidSymbolError, FetchError

router = APIRouter()

# ----------------------------
# Health Check
# ----------------------------
@router.get("/health")
async def health():
    return {"status": "ok"}


# ----------------------------
# Realtime Price Endpoint
# ----------------------------
@router.get("/realtime")
async def realtime(symbol: str = Query(..., description="e.g. BTC/USDT")):
    key = f"realtime:{symbol}"

    # Try cache first
    cached = await cache.get(key)
    if cached:
        return {"cached": True, "data": cached}

    # Fetch real data with error handling
    try:
        data = await fetch_ticker(symbol)

    except InvalidSymbolError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except FetchError as e:
        raise HTTPException(status_code=502, detail=str(e))

    # Save to cache
    await cache.set(key, data, ttl=5)

    return {"cached": False, "data": data}


# ----------------------------
# Historical OHLCV Data
# ----------------------------
@router.get("/historical")
async def historical(
    symbol: str = Query(..., description="e.g. BTC/USDT"),
    interval: str = Query("1h", description="Timeframe like 1m, 5m, 1h, 1d"),
    limit: int = Query(100, description="Number of candles"),
):
    key = f"historical:{symbol}:{interval}:{limit}"

    # Try cache first
    cached = await cache.get(key)
    if cached:
        return {"cached": True, "data": cached}

    # Fetch data with robust error handling
    try:
        data = await fetch_historical(symbol, interval, limit)

    except InvalidSymbolError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except FetchError as e:
        raise HTTPException(status_code=502, detail=str(e))

    # Save to cache
    await cache.set(key, data, ttl=30)

    return {"cached": False, "data": data}
