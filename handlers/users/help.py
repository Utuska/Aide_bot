from aiogram.dispatcher.filters import Command, CommandStart
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from utils.misc import rate_limit

from loader import dp, bot, db


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
@dp.message_handler(CommandStart(deep_link="connect_bot"))
async def connect_user(message: types.Message):
    user = message.from_user
    inline_bot = await dp.bot.get_me()
    text = [
        f'Привет <b>{user.full_name}</b>',
        f'Это inline-bot <b>{inline_bot.username}</b>',
        'В инлайн режиме бот может переводить значения в',
        'дБ по мощности и амплитуде:',
        '<code>digit W</code> - для перевода значения в <b>дБВт</b>',
        '<code>digit V</code> - для перевода значения в <b>дБВ</b>',
        '',
        'Бот выведет расписание на завтра в РЛ1 командами:',
        '<code>рас(писание) number_group</code>',
        '<code>sche(dule) number_group</code>',
        '<i>Символы в скобках писать не обязательно</i>.',
        'Задать свою группу боту можно командой /party.',
        'Помощь по командам обычного режима /common_help'
    ]
    await message.answer('\n'.join(text))


@dp.message_handler(Command(commands=['common_help']))
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '<code>/help</code> - Получить справку по inline режиму',
        '<code>/(таблица) час(тот)</code> - Получить таблицу частот (для полного набора частот команда /all)',
        '<code>/party</code> - Указать свою группу',
        '<code>/break</code> - Удалить все состояния и кнопки',
        '<code>/articles</code> - Показать полезные статьи поботам'
        'Список текстовых команд:',
        '<code>"(таблица) час(тот)"</code> - Получить таблицу частот (для полного набора частот команда /all)',
        '<code>"Отмена"</code> - Удалить все состояния и кнопки',
        '<code>"Articles"</code> - Показать полезные статьи по ботам'

    ]
    await message.answer('\n'.join(text))
