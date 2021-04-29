from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart, Text
from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import user_keyboard
from loader import dp, bot, db
from re import compile


@dp.message_handler(CommandStart(deep_link="connect_user"))
async def connect_user(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.full_name)
    await message.answer("Вы подключены")


@dp.message_handler(CommandStart(deep_link="number_party"))
@dp.message_handler(Command("party"))
async def update_email(message: types.Message, state: FSMContext):
    await message.answer("Пришли мне свою группу", reply_markup=user_keyboard.keyboard)
    await state.set_state("number_party")


#@dp.message_handler(Text(contains="Отмена", ignore_case=True))
#@dp.message_handler(Command(commands=["break"]))
# @dp.message_handler(text="Отмена")
# async def break_state(message: types.Message, state: FSMContext):
#     print("Отмена")
#     await state.finish()
#     await message.reply(text="Произведена отмена ввода. Кнопки клавиатуры удалены. Состояние обновлено.", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state="number_party")
async def enter_email(message: types.Message, state: FSMContext):
    number_party = message.text
    print("Группа")
    if number_party in ['101', '102', '103', '104', '105']:
        db.update_number_party(number_party=number_party, id=message.from_user.id)
        user = db.select_user(id=message.from_user.id)
        await message.answer(f"Данные обновлены. Запись в БД: {user}", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.reply(text=f"Такой группы не существует, укажи группу еще раз или нажми кнопку отмена",
                            reply_markup=user_keyboard.keyboard)

