import aiogram.types
from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_connector import dp, bot
from crud_functions import *
from keyboards import kb, ikb, buy_kb, build_kb, KB_UNREGISTERED, KB_REGISTERED
from utils import mifflin_san_geor, get_user_name, check_username


############ Глобальные переменные ##############

# Состояния FSM
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


################ Обработчик команды /start #####################
# @dp.message_handler(commands=lambda message: message.text and any([gs_ in message.text.lower() for gs_ in
#                                                                    ['start', 'старт']]))
@dp.message_handler(commands=['start', 'старт'])
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


################ Обработчики основной клавиатуры #####################

# ---------- Рассчитать калории -------------
@dp.message_handler(text='Рассчитать калории')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=ikb)  ### Переход на обработчик КА "Расчёт калорий"


# ---------- Регистрация или Купить -------------
################ Обработчик покупок ##################
# ---------- Купить -------------
@dp.message_handler(text='Купить')
async def get_buying_list(message: aiogram.types.Message):
    for p_ in products:
        with open(p_[IMG_FILE], 'rb') as img:
            await message.answer_photo(img, f'Название: {p_[TITLE]} | Описание: {p_[DESCRIPTION]} '
                                            f'| Цена: {p_[PRICE]}')
    await message.answer(text='Выберите продукт для покупки:', reply_markup=buy_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(text='Вы успешно приобрели продукт!')


################ Обработчик регистрации ##################
# ---------- Регистрация -------------
@dp.message_handler(text='Регистрация')
# async def sign_up(message: types.Message, state:FSMContext):
async def sign_up(message: types.Message):
    if message.from_user.username:
        await dp.storage.update_data(username=message.from_user.username, chat=message.chat.id)
        await message.answer(f'Регистрация. Твоё имя пользователя будет "{message.from_user.username}", как в Telegram.\n'
                             f'Укажи адрес электронной почты:')
        await RegistrationState.email.set()
    else:
        await message.answer(f'Регистрация. {await get_user_name(message)}'
                             f', выбери имя пользователя (только латинские буквы, цифры и "_"):')
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state):
    res = await check_username(message.text)
    while res:
        await message.answer(f'{res}\n{await get_user_name(message)}'
                             f', выбери имя пользователя (только латинские буквы, цифры и "_"):')
        res = await check_username(message.text)
    await state.update_data(username=message.text)
    await message.answer(f'Укажи адрес электронной почты:')
    await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state):
    await state.update_data(email=message.text)
    await message.answer(text='Укажи свой возраст (лет):')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age_reg(message: types.Message, state):
    age = None
    while not age:
        try:
            await state.update_data(age=message.text)
            age = int(message.text)
        except ValueError as e:
            await message.answer(text=f'{e}. Введи возраст (целое число лет):')
            message.text = None
    data = await state.get_data()
    try:
        name = data['username']
    except KeyError:
        name = message.from_user.username
    register_user(message.from_id, name, data['email'], data['age'])
    await state.finish()
    kb_user = build_kb(KB_REGISTERED)
    await bot.send_message(message.from_user.id, text='Регистрация завершена.'
                           , reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text=f'{name}, теперь ты можешь совершать покупки в нашем магазине!',
                         reply_markup=kb_user)


# ---------- Информация -------------
@dp.message_handler(text='Информация')
async def bot_info(message):
    await message.answer('''
    Бот умеет рассчитывать суточную норму калорий в зависимости от веса, роста, возраста и пола человека.
    Для расчёта используется упрощённая формула Миффлина-Сан Жеора:

     Для мужчин: 10 х вес (кг) + 6.25 x рост (см) – 5 х возраст (г) + 5.1

     Для женщин: 10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161.

    ''')


# ---------- Выход -------------
@dp.message_handler(text='Выход')
async def exit_bot(message):
    if is_logged_in(message.from_id):
    # await message.answer('До свидания!', markup=types.ReplyKeyboardRemove())
        await bot.send_message(message.from_user.id, f'До свидания, {await get_user_name(message)}!',
                               reply_markup=types.ReplyKeyboardRemove())
        exit_user(message.from_id)


########## Обработчик расчёта суточной нормы калорий #############

# ---------- Формулы -------------
@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(
        '''
        Для расчёта используется упрощённая формула Миффлина-Сан Жеора:
        Для мужчин: 10 х вес (кг) + 6.25 x рост (см) – 5 х возраст (г) + 5.1
        Для женщин: 10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161.
        '''
    )
    await call.answer()


# --------- КА Расчёта суточной нормы калорий ------
@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer(f'Введи свой возраст')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f'Введи свой рост (см)')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f'Введи свой вес (кг)')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    await message.answer(f'Ты мужчина или женщина?')
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def send_calories(message, state):
    await state.update_data(gender=message.text)
    data = await state.get_data()
    await message.answer(f'Твоя норма калорий =  {await mifflin_san_geor(**data)}.\n\n')
    await state.finish()


############## Обработчик прочих сообщений ###################
@dp.message_handler(lambda message: message.text and any([gs_ in message.text.lower() for gs_ in
                                                          ['привет', "здорово", "здравствуй", "салют",
                                                           'hi', 'hello', 'how are you', 'how do you do']]))
async def greeting_messages(message):
    await message.answer(f"Привет, коли не шутишь!")


@dp.message_handler()
async def all_messages(message):
    if is_logged_in(message.from_id):
        await message.answer(f'"{message.text}" не является командой.\nБот управляется кнопками.>')
    else:
        await message.answer('Введи команду /start, чтобы начать общение.')


if __name__ == '__main__':
    initiate_db()
    products = get_all_products()
    executor.start_polling(dp, skip_updates=True)
