from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot_config import database


homework_router = Router()


class HomeworkForm(StatesGroup):
    name = State()
    group_number = State()
    hw_number = State()
    github_link = State()
    confirmation = State()


@homework_router.callback_query(F.data == "homework")
async def homework_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(HomeworkForm.name)
    await callback.message.answer("Введите Ваше имя")


@homework_router.message(HomeworkForm.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    if not name.isalpha():
        await message.answer("Введите корректные данные")
        return
    await state.update_data(name=name)
    await state.set_state(HomeworkForm.group_number)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="46-1"),
                types.KeyboardButton(text="46-2")
            ],
            [
                types.KeyboardButton(text="47-1"),
                types.KeyboardButton(text="47-2")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("Введите номер Вашей группы", reply_markup=kb)


@homework_router.message(HomeworkForm.group_number)
async def process_group(message: types.Message, state: FSMContext):
    await state.update_data(group_number=message.text)
    await state.set_state(HomeworkForm.hw_number)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="1"),
                types.KeyboardButton(text="2"),
                types.KeyboardButton(text="3"),
                types.KeyboardButton(text="4")
            ],
            [
                types.KeyboardButton(text="5"),
                types.KeyboardButton(text="6"),
                types.KeyboardButton(text="7"),
                types.KeyboardButton(text="8")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("Введите номер домашнего задания", reply_markup=kb)


@homework_router.message(HomeworkForm.hw_number)
async def process_hw_number(message: types.Message, state: FSMContext):
    hw_number = message.text
    kb = types.ReplyKeyboardRemove()
    if not hw_number.isnumeric() or 8 < int(hw_number) < 1:
        await message.answer("Введите корректный номер задания")
        return
    await state.update_data(hw_number=hw_number)
    await state.set_state(HomeworkForm.github_link)
    await message.answer("Введите ссылку на github-репозиторий", reply_markup=kb)


@homework_router.message(HomeworkForm.github_link)
async def process_github_link(message: types.Message, state: FSMContext):
    github_link = message.text
    if github_link[:18] != "https://github.com":
        await message.answer("Введите корректную ссылку")
        print(github_link[:18], "https://github.com")
        return
    await state.update_data(github_link=github_link)
    data = await state.get_data()
    print(data)
    await message.answer(f"Имя {data["name"]}\n"
                         f"Номер группы: {data["group_number"]}\n"
                         f"Номер задания: {data["hw_number"]}\n"
                         f"Ссылка на github-репозиторий: {data["github_link"]}")
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Да"),
                types.KeyboardButton(text="Нет")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("Отправить домашнее задание?", reply_markup=kb)
    await state.set_state(HomeworkForm.confirmation)


@homework_router.message(HomeworkForm.confirmation, F.text == "Да")
async def process_confirmation_yes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sql = f"""
            INSERT INTO homeworks (name, group_number, hw_number, github_link) VALUES 
            ('{data["name"]}',
            '{data["group_number"]}',
            {data["hw_number"]},
            '{data["github_link"]}'
            )
            """
    database.execution(sql)
    kb = types.ReplyKeyboardRemove()
    database.execution(sql)
    await message.answer("Домашнее задание отправлено", reply_markup=kb)
    await state.clear()


@homework_router.message(HomeworkForm.confirmation, F.text == "Нет")
async def process_confirmaton_no(message: types.Message, state: FSMContext):
    await state.clear()
    kb = types.ReplyKeyboardRemove()
    await state.set_state(HomeworkForm.name)
    await message.answer("Введите Ваше имя", reply_markup=kb)
