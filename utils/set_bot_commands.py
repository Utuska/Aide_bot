from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Команда старта"),
        types.BotCommand("common_help", "Команда помощи в обычном режиме"),
        types.BotCommand("help", "Команда помощи в inline режиме"),
        types.BotCommand("party", "Указать свою группу"),
        types.BotCommand("break", "Удалить все состояния и кнопки"),
        types.BotCommand("articles", "Вывести статьи по ботам")
    ])

# types.BotCommand("secret", "Супер секретная команда"),
# types.BotCommand("form", "Начать опрос"),
# types.BotCommand("items", "Inline кнопки")