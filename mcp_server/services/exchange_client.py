import ccxt.async_support as ccxt
from mcp_server.services.errors import ExchangeError, InvalidSymbolError, FetchError

# Create exchange instance (we use Binance as default)
exchange = ccxt.binance({
    "enableRateLimit": True
})

async def fetch_ticker(symbol: str):
    try:
        await exchange.load_markets()

        if symbol not in exchange.symbols:
            raise InvalidSymbolError(f"Symbol not found: {symbol}")

        ticker = await exchange.fetch_ticker(symbol)
        return {
            "symbol": symbol,
            "price": ticker["last"],
            "timestamp": ticker["timestamp"],
            "exchange": "binance"
        }

    except InvalidSymbolError:
        raise
    except Exception as e:
        raise FetchError(str(e))


async def fetch_historical(symbol: str, interval: str = "1h", limit: int = 100):
    try:
        await exchange.load_markets()

        if symbol not in exchange.symbols:
            raise InvalidSymbolError(f"Symbol not found: {symbol}")

        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe=interval, limit=limit)

        return [
            {
                "timestamp": c[0],
                "open": c[1],
                "high": c[2],
                "low": c[3],
                "close": c[4],
                "volume": c[5],
            }
            for c in ohlcv
        ]

    except InvalidSymbolError:
        raise
    except Exception as e:
        raise FetchError(str(e))
