from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

translation_values = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Перевести и записать переменную")
        ],
        [
            KeyboardButton(text="Показать все свои предыдущие записи"),
            KeyboardButton(text="Отмена")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)