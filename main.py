from aiogram import executor, types

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from crud_functions import *
from handlers.Main_Menu import greeting_messages
from config import *
from handlers import Calories, Main_Menu, Registration

bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


################ Обработчик команды /start #####################
dp.message_handler(commands=['start', 'старт'])(callback=Main_Menu.start)

################ Обработчики основной клавиатуры #####################
dp.message_handler(text='Рассчитать калории')(callback=Main_Menu.main_menu)
dp.message_handler(text='Купить')(callback=Main_Menu.get_buying_list)
dp.message_handler(text='Регистрация')(callback=Registration.sign_up)
dp.message_handler(text='Информация')(callback=Main_Menu.bot_info)
dp.message_handler(text='Выход')(callback=Main_Menu.exit_bot)

############## Обработчик приветственного и прочих сообщений ##################
dp.message_handler(lambda message: message.text and any([gs_ in message.text.lower() for gs_ in
                    ['привет', "здорово", "здравствуй", "салют",
                     'hi', 'hello', 'how are you', 'how do you do']]))(callback=greeting_messages)
dp.message_handler()(callback=Main_Menu.all_messages)


################ Обработчик регистрации ##################
dp.message_handler(state=Registration.RegistrationState.username)(callback=Registration.set_username)
dp.message_handler(state=Registration.RegistrationState.email)(callback=Registration.set_email)
dp.message_handler(state=Registration.RegistrationState.age)(callback=Registration.set_age_reg)


################# Обработчик покупок ###############
dp.callback_query_handler(text='product_buying')(callback=Main_Menu.send_confirm_message)


######### Обработчик расчёта суточной нормы калорий #############
# ---------- Формулы -------------
dp.callback_query_handler(text='formulas')(callback=Calories.get_formulas)
# --------- КА Расчёта суточной нормы калорий ------
dp.callback_query_handler(text='calories')(callback=Calories.set_age)
dp.message_handler(state=Calories.UserState.age)(callback=Calories.set_growth)
dp.message_handler(state=Calories.UserState.growth)(callback=Calories.set_weight)
dp.message_handler(state=Calories.UserState.weight)(callback=Calories.set_gender)
dp.message_handler(state=Calories.UserState.gender)(callback=Calories.send_calories)


if __name__ == '__main__':
    products = get_all_products()
    executor.start_polling(dp, skip_updates=True)
