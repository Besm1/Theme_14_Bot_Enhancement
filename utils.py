from aiogram import types
from aiogram.types import Message
from crud_functions import get_user_info, U_USERNAME, U_FIRST_NAME, U_LAST_NAME, user_exists, is_logged_in


async def mifflin_san_geor(age, growth, weight, gender):
    '''
    Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5. 1
    Для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.
    :param age: - возраст, лет
    :param growth: - рост, см
    :param weight: - вес, кг
    :param gender: - м(ужчина) или ж(енщина)
    :return: - суточная норма калорий, кал
    '''
    try:
        res = (10 * float(weight)  + 6.25 * float(growth)
               - 5 * float(age)
               + (5.1 if gender[0].lower() == 'м' else (-161 if gender[0].lower() == 'ж' else None)))
    except Exception as e:
        res = f'...Упссс! Неправильные данные привели к ошибке: "{e}". Не могу рассчитать...'
    finally:
        return res

async def get_user_name(message:Message):
    name = '"NoName"'
    if message.from_user.username:
        name = message.from_user.username
    else:
        uinfo = get_user_info(message.from_id)
        if uinfo[U_USERNAME]:
            name = uinfo[U_USERNAME]
        elif uinfo[U_FIRST_NAME]:
            name = uinfo[U_FIRST_NAME]
        elif uinfo[U_LAST_NAME]:
            name = uinfo[U_LAST_NAME]
    return name

async def check_username(text:str):
    ret = None
    # if not all([c_ == '_' or ord('a') <= ord(c_.lower()) <= ord('z') or c_.isdigit() for c_ in text]):
    if not text.replace('_', '').isalnum():
        ret = 'Имя должно содержать только латинские буквы, цифры и "_"'
    elif user_exists(text):
        ret = f'Имя пользователя "{text}" занято.'
    return ret


async def all_messages(message):
    if is_logged_in(message.from_id):
        await message.answer(f'"{message.text}" не является командой.\nБот управляется кнопками.>')
    else:
        await message.answer('Введи команду /start, чтобы начать общение.', reply_markup=types.ReplyKeyboardRemove())

