from fastapi import FastAPI
from mcp_server.routes import router

app = FastAPI(title="MCP Crypto Server - Beginner Version")

app.include_router(router)
