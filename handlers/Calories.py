from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

from utils import mifflin_san_geor

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


async def get_formulas(call):
    await call.message.answer(
        '''
        Для расчёта используется упрощённая формула Миффлина-Сан Жеора:
        Для мужчин: 10 х вес (кг) + 6.25 x рост (см) – 5 х возраст (г) + 5.1
        Для женщин: 10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161.
        '''
    )
    await call.answer()


async def set_age(call):
    await call.message.answer(f'Введи свой возраст')
    await call.answer()
    await UserState.age.set()


async def set_weight(message:types.Message, state):
    if not message.text.isnumeric() or int(message.text) <= 0:
        await message.answer(f'Введи свой возраст - положительное число:')
        return
    await state.update_data(age=message.text)
    await message.answer(f'Введи свой рост (см)')
    await UserState.growth.set()


async def set_growth(message, state):
    if not message.text.isnumeric() or int(message.text) <= 100:
        await message.answer(f'Введи свой рост (> 100):')
        return
    await state.update_data(growth=message.text)
    await message.answer(f'Введи свой вес (кг)')
    await UserState.weight.set()


async def set_gender(message, state):
    if not message.text.isnumeric() or int(message.text) <= 20:
        await message.answer(f'Введи свой вес (> 20):')
        return
    await state.update_data(weight=message.text)
    await message.answer(f'Ты мужчина или женщина?')
    await UserState.gender.set()


async def send_calories(message:types.Message, state):
    if not message.text.lower() in ['мужчина'[0:(len(message.text) if len(message.text) <= len('мужчина') else len('мужчина'))]
    , 'женщина'[0:(len(message.text) if len(message.text) <= len('женщина') else len('женщина'))]]:
        await message.answer(f'Ты мужчина или женщина?')
        return
    await state.update_data(gender=message.text)
    data = await state.get_data()
    await message.answer(f'Твоя норма калорий =  {await mifflin_san_geor(**data)}.\n\n')
    await state.finish()

