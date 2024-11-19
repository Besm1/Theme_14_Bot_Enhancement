from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup


# Подготовка основной клавиатуры
kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рассчитать калории')]
    , [KeyboardButton(text='Купить')]
    , [KeyboardButton(text='Информация')]
    , [KeyboardButton(text='Выход')]
 ]
,  resize_keyboard=True)

KB_REGISTERED = ['Рассчитать калории', 'Купить', 'Информация', 'Выход']
KB_UNREGISTERED = ['Рассчитать калории', 'Регистрация', 'Информация', 'Выход']

def build_kb(menu_list) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for el in menu_list:
        kb.add(KeyboardButton(text=el))
    return kb


# btn_calculate = KeyboardButton(text='Рассчитать')
# btn_info = KeyboardButton(text='Информация')
# kb.add(btn_calculate)
# kb.add(btn_info)

# Подготовка InLine клавиатур

# Клава расчёта
ikb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Рассчитать норму калорий',callback_data='calories')]
                               ,[InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]])

# Клава покупки товаров
# buy_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Product1',callback_data='product_buying')]
#     , [InlineKeyboardButton(text='Product2',callback_data='product_buying')]
#     , [InlineKeyboardButton(text='Product3',callback_data='product_buying')]
#     , [InlineKeyboardButton(text='Product4',callback_data='product_buying')]
# ])
buy_kb = InlineKeyboardMarkup()
buy_kb.insert(InlineKeyboardButton(text='Product1',callback_data='product_buying'))
buy_kb.insert(InlineKeyboardButton(text='Product2',callback_data='product_buying'))
buy_kb.insert(InlineKeyboardButton(text='Product3',callback_data='product_buying'))
buy_kb.insert(InlineKeyboardButton(text='Product4',callback_data='product_buying'))