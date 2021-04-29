from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

general_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                       keyboard=[
                                           [
                                               KeyboardButton(text="Да"), KeyboardButton(text="Нет")
                                           ],
                                           [
                                               KeyboardButton(text="Отмена")
                                           ]
                                       ])