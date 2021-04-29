from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

callback_information = CallbackData("buy", "item_name", "id_item")
callback_like = CallbackData("like", "command", "id_item", "action")



def item_keyboard(db: dict):
    commodity_field = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            InlineKeyboardButton(text="Мощность",
                                 callback_data=callback_information.new(item_name=db['name'], id_item=db['item_id']))
        ],
        [
            InlineKeyboardButton(text='Мощность', callback_data=callback_like.new(command="like",
                                                                                  id_item=db['item_id'],
                                                                                  action=int(db['count_like']) + 1)),
            InlineKeyboardButton(text='Ток', callback_data=callback_like.new(command="dislike",
                                                                             id_item=db['item_id'],
                                                                             action=int(db['count_like']) - 1))
        ],
        [
            InlineKeyboardButton(text='Колличество пользователей', callback_data='count')
        ],
        [
            InlineKeyboardButton(text='Поделиться с другом', callback_data='share')
        ]])
    return commodity_field
