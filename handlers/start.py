from aiogram import Router, types, F
from aiogram.filters.command import Command


start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    kb = types.InlineKeyboardMarkup(
        inline_keyboard =[
            [
                types.InlineKeyboardButton(text="Отправить домашнее задание", callback_data="homework")
            ]
        ]
    )
    await message.answer(f"Здравствуйте, {message.from_user.first_name}!", reply_markup=kb)


