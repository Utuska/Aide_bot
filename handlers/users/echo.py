from aiogram import types
from loader import dp


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def bot_echo(message: types.Message):
    chat_id = message.from_user.id
    text = f"Пользователь {message.from_user.full_name} написал {message.text}"
    await dp.bot.send_message(chat_id=chat_id, text=text)
    bot_user = await dp.bot.get_me()
    name_bot = bot_user.username
    text = f"Бот {name_bot} ответил пользователю {message.text}"
    await message.answer(text)
