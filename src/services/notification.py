from src.redis.pubsub import publish_deal


async def publish_new_deal(deal_data: dict):
    await publish_deal(deal_data)
