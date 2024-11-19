from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import aiogram

from crud_functions import *
from keyboards import *
from utils import all_messages


async def start(message: types.Message):
    start_user(message.from_user)
    if is_registered(message.from_id):
        kb_user = build_kb(KB_REGISTERED)
        regtxt = ""
    else:
        kb_user = build_kb(KB_UNREGISTERED)
        regtxt = "\n(Чтобы купить что-нибудь в нашем магазине, надо зарегистрироваться)"  # "Довесок" к тексту приветствия в случае отсутствия регистрации
    await message.answer("Привет! Я Бот, который заботится о твоём здоровье.\n"
                         "Для управления воспользуйся кнопками внизу.\n"
                         "Могу рассчитать твою суточную норму калорий или помочь в покупке товаров для здоровья."
                         + regtxt
                         , reply_markup=kb_user)


async def get_buying_list(message: aiogram.types.Message):
    if not is_logged_in(message.from_id):
        await all_messages(message)
    else:
        for p_ in products:
            with open('files\\images\\' + p_[IMG_FILE], 'rb') as img:
                await message.answer_photo(img, f'Название: {p_[TITLE]} | Описание: {p_[DESCRIPTION]} '
                                                f'| Цена: {p_[PRICE]}')
        await message.answer(text='Выберите продукт для покупки:', reply_markup=buy_kb)


async def send_confirm_message(call):
    await call.message.answer(text='Вы успешно приобрели продукт!')


async def bot_info(message):
    if not is_logged_in(message.from_id):
        await all_messages(message)
    else:
        await message.answer('''
        Бот умеет рассчитывать суточную норму калорий в зависимости от веса, роста, возраста и пола человека.
        Для расчёта используется упрощённая формула Миффлина-Сан Жеора:

         Для мужчин: 10 х вес (кг) + 6.25 x рост (см) – 5 х возраст (г) + 5.1

         Для женщин: 10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161.

        ''')


async def exit_bot(message):
    if not is_logged_in(message.from_id):
        await all_messages(message)
    else:
        if is_logged_in(message.from_id):
            await message.answer(f'До свидания, {get_user_info(message.from_id)[U_USERNAME]}!',
                                   reply_markup=types.ReplyKeyboardRemove())
            # await bot.send_message(message.from_user.id, f'До свидания, {await get_user_name(message)}!',
            #                        reply_markup=types.ReplyKeyboardRemove())
            exit_user(message.from_id)


#
async def main_menu(message):
    if not is_logged_in(message.from_id):
        await all_messages(message)
    else:
        await message.answer('Выберите опцию', reply_markup=ikb)  ### Переход на обработчик КА "Расчёт калорий"


async def greeting_messages(message):
    await message.answer(f"Привет, коли не шутишь!")



