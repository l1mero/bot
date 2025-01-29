from aiogram import Router
from aiogram.types import Message

from db.models.user import User

router = Router()

@router.message()
async def echo_handler(message: Message, user: User) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        await message.answer(f"ИДИ НАХУЙ")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

router_nahui = router