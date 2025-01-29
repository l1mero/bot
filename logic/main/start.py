from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from db.models.user import User
from db import users
from datetime import datetime

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message, user: User | None) -> None:
    """
    This handler receives messages with `/start` command
    """
    if not user:
        user = User(
            tg_id=message.from_user.id,
            date=datetime.now()
        ).model_dump(by_alias=True)

        await users.insert_one(user)


    await message.answer(f"Hello, {message.from_user.full_name}! Ты ебаный пидорас!")

router_start = router