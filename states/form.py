from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    name_step = State()
    email_step = State()
    phone_step = State()