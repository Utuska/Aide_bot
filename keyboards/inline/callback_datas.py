from aiogram.utils.callback_data import CallbackData

callback_information = CallbackData("buy", "item_name", "id_item")
callback_like = CallbackData("like", "command", "id_item", "action")