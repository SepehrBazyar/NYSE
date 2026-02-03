import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.router import router as api_router
from src.redis.pubsub import (
    close_redis,
    init_redis,
    redis_listener,
)
from src.websocket.routes import router as ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    listener_task = asyncio.create_task(redis_listener())
    yield
    listener_task.cancel()
    await close_redis()


app = FastAPI(lifespan=lifespan, title="Real-Time Trading Notifier")

app.include_router(api_router, prefix="/api")
app.include_router(ws_router)
