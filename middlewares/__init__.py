from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .database import GetDBUsers


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(GetDBUsers())
