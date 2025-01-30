import asyncio

import redis.asyncio as redis

redis = redis.Redis(host='127.0.0.1', port=6379, password="ggbet3344")


async def main():

    await redis.set('foo', 'bar')

asyncio.run(main())