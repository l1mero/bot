import asyncio

from db import users
from db.models.user import User
from datetime import datetime
from random import randint

async def generate_test_users():
    for _ in range(10000):
        user = User(
                tg_id=randint(1000000000, 9999999999),
                date=datetime.now()
            ).model_dump(by_alias=True)

        await users.insert_one(user)

asyncio.run(generate_test_users())