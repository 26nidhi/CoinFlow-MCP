
# 🚀 MCP Crypto Market Data Server  
A Python-based MCP (Model Context Protocol) server for retrieving **real-time** and **historical** cryptocurrency market data using FastAPI, CCXT, and a lightweight caching layer.  
Built as part of an internship assignment.

---

## 📌 Features

### ✅ Core Endpoints
| Endpoint | Description |
|---------|-------------|
| `GET /health` | Health check |
| `GET /realtime?symbol=BTC/USDT` | Real-time ticker price (via CCXT, mocked in tests) |
| `GET /historical?symbol=BTC/USDT&interval=1h&limit=100` | Historical OHLCV data |

### ✅ MCP Requirements Implemented
- Clean modular Python package structure  
- Real-time data retrieval  
- Historical candlestick data  
- Custom error handling  
- In-memory caching (TTL-based)  
- Test suite with full mocking (no external API calls)  
- Reliable, deterministic tests  

---

## 📁 Project Structure

```

mcp-crypto-server/
│
├── mcp_server/
│   ├── **init**.py
│   ├── main.py
│   ├── routes.py
│   └── services/
│       ├── **init**.py
│       ├── cache.py
│       ├── exchange_client.py
│       ├── errors.py
│
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_realtime.py
│   ├── test_historical.py
│
├── requirements.txt
└── README.md

````

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/mcp-crypto-server.git
cd mcp-crypto-server
````

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
```

### 3️⃣ Activate it

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Server

Start the FastAPI server:

```bash
uvicorn mcp_server.main:app --reload --port 8000 --reload-exclude ".venv"
```

Server URL:

```
http://127.0.0.1:8000
```

---

## 📡 API Endpoints

### ✔ Health Check

```
GET /health
```

Response:

```json
{"status": "ok"}
```

---

### ✔ Real-Time Price

```
GET /realtime?symbol=BTC/USDT
```

Example:

```json
{
  "cached": false,
  "data": {
    "symbol": "BTC/USDT",
    "price": 43250.12,
    "timestamp": 123456789,
    "exchange": "binance"
  }
}
```

---

### ✔ Historical OHLCV Data

```
GET /historical?symbol=BTC/USDT&interval=1h&limit=100
```

Example:

```json
{
  "cached": false,
  "data": [
    { "timestamp": 123, "open": 1, "high": 2, "low": 1, "close": 1.5, "volume": 100 }
  ]
}
```

---

## 🧪 Running Tests

All external network calls are mocked.
Tests run fully offline.

Run tests:

```bash
pytest -q
```

Expected output:

```
5 passed in X.XXs
```

---

## 🧱 Design Decisions & Assumptions

* CCXT is used for real market data (Binance by default).
* All live network calls are **mocked** in the test suite.
* In-memory caching is sufficient for this assignment.
* Custom errors implemented:

  * `InvalidSymbolError`
  * `ExchangeDownError`
  * `HistoricalDataError`

---


