from aiogram import Dispatcher, types
from aiogram.types import Update, Message

from db.models.user import User
from db.mongo import Motor
from datetime import datetime
from db import users


class AuthMiddleware:
    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher

    async def __call__(self, handler, m: Message, data: dict):
        user = await users.find_one({"tg_id": m.from_user.id})

        if user:
            data["user"] = User(**user)

            return await handler(m, data)

        if m.text == "/start":
            data["user"] = None

            return await handler(m, data)

        return await m.answer("АЛОООООООООООООО ДОДИК НАПИШИ /start")
