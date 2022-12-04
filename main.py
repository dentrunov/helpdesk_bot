import sqlite3
from datetime import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.builtin import IDFilter, CommandStart

from config import TOKEN
import keyb as kb

from db_connect import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

first = False
t = 0


async def on_startup(_):
    await db_start()


@dp.message_handler(CommandStart())
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    if check_last_t(user_id):
        if user_id == adm():
            await bot.send_message(adm(), "Административный доступ", reply_markup=kb.ReplyKeyboardRemove())
        else:
            await message.answer("Здравствуйте, это бот поддержки электронного журнала школы Ника.",
                             reply_markup=kb.greet_kb)
    else:
        await message.answer("Здравствуйте, это бот поддержки электронного журнала школы Ника. Вы впервые воспользовались ботом, просим зарегистрироваться", reply_markup=kb.new_kb)

#запрос на открытие доступа, TODO уйти от глобальных переменных
@dp.message_handler(lambda message: message.text == 'Открыть доступ')
async def task_open(message: types.Message):
    global t
    t = 1
    await message.answer("Кратко опишите проблему", reply_markup=kb.ReplyKeyboardRemove())

#разрешение открытия доступа
@dp.callback_query_handler(lambda c: c.data == 'confirm')
async def process_callback_confirm(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    num = callback_query.message.text.split()[-1]
    await confirm_task(num)
    await bot.send_message(callback_query.from_user.id, 'Одобрено')


@dp.message_handler(lambda message: message.text == 'Другие проблемы')
async def task_other(message: types.Message):
    global t
    t = 2
    await message.answer("Кратко опишите проблему", reply_markup=kb.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == 'Проверить заявку')
async def task_check(message: types.Message):
    await message.answer("Пока не работает", reply_markup=kb.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == 'Одобрить')
async def task_conf(message: types.Message):

    await message.answer("Кратко опишите проблему", reply_markup=kb.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == 'Зарегистрироваться')
async def reg_message(message: types.Message):
    global first
    first = True
    await message.answer("Просим представиться", reply_markup=kb.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text == 'Назад')
async def reg_message(message: types.Message):
    first = True
    await message.answer("Главное меню",  reply_markup=kb.greet_kb)

@dp.message_handler(content_types=types.ContentType.TEXT)
async def cur_message(message: types.Message):
    global first, t
    user_id = message.from_user.id
    mess = message.text
    #Скрипт регистрации
    if first:
        first = False
        await message.answer("Вы зарегистрированы", reply_markup=kb.greet_kb)
        await new_t(user_id, mess, user_id)
    else:
        #админ доступ
        if user_id == adm():
            await bot.send_message(adm(), "Административный доступ", reply_markup=kb.ReplyKeyboardRemove())
        #отправка заявки на открытие доступа
        if t == 1:
            a = adm()
            num = await save_task(user_id, 0, mess)
            await message.answer("Ваша заявка оправлена!", reply_markup=kb.ReplyKeyboardRemove())
            m = f'Заявка от {get_t(user_id)[1]}\n{mess}\nНомер заявки {num} '
            await bot.send_message(a, m, reply_markup=kb.conf_kb)
        elif t == 2:
            pass
            t = 0
            await message.answer("Ничего", reply_markup=kb.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)