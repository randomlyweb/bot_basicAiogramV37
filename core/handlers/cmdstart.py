from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from core.db.db import add_user


router = Router()


@router.message(CommandStart())
async def say_hello(message: Message):
    await add_user(message.from_user.id)
    await message.answer('Hello!')


@router.callback_query(F.data == 'start')
async def say_hello_callback(call: CallbackQuery):
    await call.message.delete()
    await add_user(call.from_user.id)
    await call.message.answer('Hello!')
