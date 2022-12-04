from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


back_button = KeyboardButton('Назад')

button_marks = KeyboardButton('Открыть доступ')
button_problems = KeyboardButton('Другие проблемы')
button_check = KeyboardButton('Проверить заявку')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(button_marks, button_problems, button_check, back_button)

button_reg = KeyboardButton('Зарегистрироваться')
new_kb = ReplyKeyboardMarkup(resize_keyboard=True,).add(button_reg)

button_conf = InlineKeyboardButton('Одобрить', callback_data='confirm')
conf_kb = InlineKeyboardMarkup(resize_keyboard=True,).add(button_conf)

