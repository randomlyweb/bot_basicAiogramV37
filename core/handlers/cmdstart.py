from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from core.db.db import add_user
from core.keyboards.client_kb import start_kb


router = Router()


@router.message(CommandStart())
async def say_hello(message: Message):
    await add_user(message.from_user.id)
    await message.answer('Привет! Добро пожаловать в бота для просмотра актуальных квизов', reply_markup=start_kb())


@router.callback_query(F.data == 'start')
async def say_hello_callback(call: CallbackQuery):
    await call.message.delete()
    await add_user(call.from_user.id)
    await call.message.answer('Привет! Добро пожаловать в бота для просмотра актуальных квизов', reply_markup=start_kb())