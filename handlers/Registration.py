from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

from utils import all_messages, get_user_name, check_username
from crud_functions import is_logged_in, register_user
from keyboards import build_kb, KB_REGISTERED

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

async def sign_up(message: types.Message, state):
    if not is_logged_in(message.from_id):
        await all_messages(message)
    else:
        if message.from_user.username:
            await state.update_data(username=message.from_user.username) #, chat=message.chat.id)
            # await dp.storage.update_data(username=message.from_user.username, chat=message.chat.id)
            await message.answer(f'Регистрация. Твоё имя пользователя будет "{message.from_user.username}", как в Telegram.\n'
                                 f'Укажи адрес электронной почты:')
            await RegistrationState.email.set()
        else:
            await message.answer(f'Регистрация. {await get_user_name(message)}'
                                 f', выбери имя пользователя (только латинские буквы, цифры и "_"):')
            await RegistrationState.username.set()


async def set_username(message: types.Message, state):
    res = await check_username(message.text)
    if res:
        await message.answer(f'{res}\nвыбери имя пользователя (только латинские буквы, цифры и "_"):')
        return
    await state.update_data(username=message.text)
    await message.answer(f'Укажи адрес электронной почты:')
    await RegistrationState.email.set()


async def set_email(message: types.Message, state):
    await state.update_data(email=message.text)
    await message.answer(text='Укажи свой возраст (лет):')
    await RegistrationState.age.set()


async def set_age_reg(message: types.Message, state):
    if not message.text.isnumeric() or int(message.text) <= 0:
        await message.answer(f'Введи свой возраст - положительное число:')
        return
    await state.update_data(age=int(message.text))
    data = await state.get_data()
    try:
        name = data['username']
    except KeyError:
        name = message.from_user.username
    register_user(message.from_id, name, data['email'], data['age'])
    await state.finish()
    kb_user = build_kb(KB_REGISTERED)
    await message.answer(text='Регистрация завершена.'
                           , reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text=f'{name}, теперь ты можешь совершать покупки в нашем магазине!',
                         reply_markup=kb_user)

