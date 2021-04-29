from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart, Text
from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from loader import dp, bot, db


@dp.message_handler(Text(contains="Отмена", ignore_case=True), state="number_party")
@dp.message_handler(Command(commands=["break"]), state="number_party")
@dp.message_handler(Command(commands=["break"]))
async def break_state(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(text="Произведена отмена ввода. Кнопки клавиатуры удалены. Состояние обновлено.", reply_markup=ReplyKeyboardRemove())