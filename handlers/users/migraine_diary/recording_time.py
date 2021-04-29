import pytz

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import re
from aiogram.dispatcher.filters import Command, CommandStart, RegexpCommandsFilter, Text
from aiogram.types import InputFile, ReplyKeyboardMarkup, KeyboardButton
from loader import dp, bot, db, scheduler


async def migraine_record(dp: Dispatcher, id, state: FSMContext):
    text = f"Введи запись в журнал мигрени."
    await dp.bot.send_message(chat_id=id, text=text)
    await state.set_state("record")


async def schedule_jobs(id, state):
    user = db.select_user(id=id)

    time = user[4]
    print(time)
    hour = int(f'{time[0]}{time[1]}')
    print(hour)
    minute = int(f'{time[3]}{time[4]}')
    print(minute)

    scheduler.add_job(migraine_record, 'cron', day_of_week='mon-sun', hour=hour, minute=minute,
                      timezone=pytz.timezone('Europe/Moscow'),
                      args=(dp, id, state))


@dp.message_handler(Command("set_time"))
async def update_email(message: types.Message, state: FSMContext):
    await message.answer("Введите время в формате ЧЧ:ММ по Москве.")
    await state.set_state("set_time")


@dp.message_handler(state="set_time")
async def enter_time(message: types.Message, state: FSMContext):
    time = message.text
    if re.match(r'[0-2]?[0-9]{1}[.:-]{1}[0-9]{2}', time) and len(time) <= 5:
        print(time)
        db.update_user_time(time=time, id=message.from_user.id)
        user = db.select_user(id=message.from_user.id)
        await message.answer(f"Данные обновлены. Запись в БД: {user}")
        await state.finish()
        await schedule_jobs(message.from_user.id, state)
    else:
        await message.reply(text=f"Некорректный ввод времени. Попробуйте еще раз.")