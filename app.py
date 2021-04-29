from utils import set_default_commands
from loader import db, scheduler

from aiogram import Dispatcher


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify

    try:
        db.create_table_users()
        db.create_table_schedule_migraine()
    except Exception as e:
        print(e)

    #db.delete_users()
    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
