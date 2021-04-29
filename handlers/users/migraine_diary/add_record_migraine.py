from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from keyboards.default import list_keyboard
from loader import dp, bot, db

import datetime
import pytz


@dp.message_handler(Command("record"))
async def start_input(message: types.Message, state: FSMContext):
    await message.answer("Введи запись в журнал")
    await state.set_state("record")


@dp.message_handler(Text(contains="Да", ignore_case=True), state="record")
async def confirm_entry_yes(message: types.Message, state: FSMContext):
    await message.answer(f"Запись в дневник произведена", reply_markup=ReplyKeyboardRemove())
    print(db.select_all_recording())
    await state.finish()


@dp.message_handler(Text(contains="Нет", ignore_case=True), state="record")
async def confirm_entry_no(message: types.Message, state: FSMContext):
    db.delete_last_record()
    await message.answer(f"Запись в дневник отменена", reply_markup=ReplyKeyboardRemove())
    print(db.select_all_recording())
    await state.finish()


@dp.message_handler(state="record")
async def enter_record(message: types.Message, state: FSMContext):
    moscow_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    db.add_recording(id_recording=message.from_user.id, date=moscow_time.date(), status=message.text)
    await message.answer(f"Подтвердить запись в дневник", reply_markup=list_keyboard.general_keyboard)
    print(db.select_all_recording())