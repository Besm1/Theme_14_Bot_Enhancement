import aiogram.types
from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_connector import dp, bot
from crud_functions import *
from keyboards import kb, ikb, buy_kb
from utils import mifflin_san_geor

is_start_pressed = False
u_name = ''

# Состояния FSM
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()

class RegistrationState(StatesGroup):
    email = State()
    age = State()
    balance = State()

################ Обработчик команды /start #####################
# @dp.message_handler(commands=lambda message: message.text and any([gs_ in message.text.lower() for gs_ in
#                                                                    ['start', 'старт']]))
@dp.message_handler(commands=['start', 'старт'])
async def start(message: types.Message):
    global is_start_pressed
    is_start_pressed = True
    if not is_inserted(message.from_user.username):
        kb.keyboard[1][0].text = 'Регистрация'
        regtxt = "\n(Чтобы купить что-нибудь, надо зарегистрироваться)"
        # await bot.send_message(message.from_user.id, '',reply_markup=types.ReplyKeyboardRemove())
    else:
        regtxt = ""

    await message.answer("Привет! Я Бот, который заботится о твоём здоровье.\n"
                    "Для управления воспользуйся кнопками внизу.\n"
                    "Могу рассчитать твою суточную норму калорий или помочь в покупке товаров для здоровья."
                    + regtxt
                     , reply_markup=kb)

################ Обработчики основной клавиатуры #####################

# ---------- Рассчитать калории -------------
@dp.message_handler(text='Рассчитать калории')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=ikb)  ### Переход на обработчик КА "Расчёт калорий"


# ---------- Регистрация или Купить -------------
@dp.message_handler(lambda message: message.text and any([message.text == txt for txt in ['Регистрация', 'Купить']]))
async def buy_or_register(message: aiogram.types.Message):
    global u_name
    u_name = message.from_user.username
    if message.text == 'Купить':
        await get_buying_list(message)
    else:
        await sign_up(message)


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
    global is_start_pressed
    # await message.answer('До свидания!', markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, 'До свидания!',reply_markup=types.ReplyKeyboardRemove())
    is_start_pressed = False


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


################ Обработчик регистрации ##################
# ---------- Регистрация -------------
async def sign_up(message: types.Message):
    global u_name
    await message.answer(f'Регистрация. {u_name}, укажи адрес электронной почты:')
    await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state):
    await state.update_data(email=message.text)
    await message.answer(text='Укажи свой возраст (лет):')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age_reg(message: types.Message, state):
    global u_name
    age = None
    while not age:
        try:
            await state.update_data(age=message.text)
            age = int(message.text)
        except ValueError as e:
            await message.answer(text=f'{e}. Введи возраст (целое число лет):')
            message.text = None
    data = await state.get_data()
    add_user(None, u_name, data['email'], data['age'])
    await state.finish()
    kb.keyboard[1][0].text = 'Купить'
    await bot.send_message(message.from_user.id, text='Регистрация завершена.'
                           , reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text=f'{u_name}, теперь ты можешь совершать покупки в нашем магазине!', reply_markup=kb)


################ Обработчик покупок ##################
# ---------- Купить -------------
async def get_buying_list(message: aiogram.types.Message):
    for p_ in products:
        with open(p_[IMG_FILE], 'rb') as img:
            await message.answer_photo(img, f'Название: {p_[TITLE]} | Описание: {p_[DESCRIPTION]} '
                                            f'| Цена: {p_[PRICE]}')
    await message.answer(text='Выберите продукт для покупки:', reply_markup=buy_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(text='Вы успешно приобрели продукт!')



############## Обработчик прочих сообщений ###################
@dp.message_handler(lambda message: message.text and any([gs_ in message.text.lower() for gs_ in
                                                          ['привет', "здорово", "здравствуй", "салют",
                                                           'hi', 'hello', 'how are you', 'how do you do']]))
async def greeting_messages(message):
    await message.answer(f"Привет, коли не шутишь!")

@dp.message_handler()
async def all_messages(message):
    global is_start_pressed
    if is_start_pressed:
        await message.answer(f'"{message.text}" не является командой.\nБот управляется кнопками.>')
    else:
        await message.answer('Введи команду /start, чтобы начать общение.')

if __name__ == '__main__':
    initiate_db()
    products = get_all_products()
    executor.start_polling(dp, skip_updates=True)
