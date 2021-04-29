from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import callback_information, callback_like


def item_keyboard(db: dict):
    commodity_field = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Купить товар",
                                 callback_data=callback_information.new(item_name=db['name'], id_item=db['item_id']))
        ],
        [
            InlineKeyboardButton(text='Лайк', callback_data=callback_like.new(command="like",
                                                                              id_item=db['item_id'],
                                                                              action=int(db['count_like']) + 1)),
            InlineKeyboardButton(text='Дизлайк', callback_data=callback_like.new(command="dislike",
                                                                                 id_item=db['item_id'],
                                                                                 action=int(db['count_like']) - 1))
        ],
        [
            InlineKeyboardButton(text='Поделиться с другом', callback_data='share')
        ]])
    return commodity_field
