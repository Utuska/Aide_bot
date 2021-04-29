import sqlite3

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from loader import db


class GetDBUsers(BaseMiddleware):

    async def on_process_message(self, message: types.Message, data: dict):
        try:
            db.add_user(id=message.from_user.id, name=message.from_user.full_name)
            pass
        except sqlite3.IntegrityError as err:
            print(err)

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        try:
            db.add_user(id=cq.from_user.id, name=cq.from_user.full_name)
            pass
        except sqlite3.IntegrityError as err:
            print(err)