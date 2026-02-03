import json

from redis.asyncio import Redis, from_url

from src.config import settings
from src.websocket.manager import manager

redis_client: Redis = None


async def init_redis():
    global redis_client
    redis_client = await from_url(settings.REDIS_URL, decode_responses=True)


async def close_redis():
    if redis_client:
        await redis_client.close()


async def publish_deal(deal_data: dict):
    if redis_client:
        await redis_client.publish("new_deals", json.dumps(deal_data))


async def redis_listener():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("new_deals")

    async for message in pubsub.listen():
        if message.get("type") == "message":
            try:
                deal = json.loads(message["data"])
                await manager.broadcast_to_tag(deal["tag_id"], deal)
            except Exception as e:
                print(f"Error in redis listener: {e}")
