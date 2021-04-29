from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart, Text
from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import user_keyboard
from loader import dp, bot, db


@dp.message_handler(Text(contains="Отмена", ignore_case=True), state="number_party")
@dp.message_handler(Text(contains="Отмена", ignore_case=True), state="record")
@dp.message_handler(Text(contains="Отмена", ignore_case=True), state="mail")
@dp.message_handler(Text(contains="Отмена", ignore_case=True) | Command(commands=['break']))
async def break_state(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(text="Произведена отмена ввода. Кнопки клавиатуры удалены. Состояние обновлено.",
                        reply_markup=ReplyKeyboardRemove())