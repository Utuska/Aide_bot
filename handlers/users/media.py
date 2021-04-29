from aiogram import types
from aiogram.dispatcher.filters import Command, CommandStart, RegexpCommandsFilter, Text
from aiogram.types import InputFile
from re import compile
from loader import dp, bot, db

REGEXP_EXPRESSION_TABLE_FREQUENCY = r'(таб(лица))?\s?час(тот)?'


@dp.message_handler(RegexpCommandsFilter([REGEXP_EXPRESSION_TABLE_FREQUENCY]))
@dp.message_handler(regexp=REGEXP_EXPRESSION_TABLE_FREQUENCY)
async def send_table(message: types.Message):
    photo_link = InputFile('photos/data.png')
    await message.answer_photo(photo=photo_link, caption='Посмотреть полную информацию /all')


@dp.message_handler(Command("all"))
async def send_all(message: types.Message):
    # Создаем альбом
    album = types.MediaGroup()

    photo_optics = "https://fibertop.ru/image/%D1%82%D1%80%D0%B0%D1%81%D1%81%D0%BE%D0%B8%D1%81%D0%BA%D0%B0%D1%82%D0%B5%D0%BB%D0%B8/fibertop_articles/%20%D0%BE%D0%BF%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B3%D0%BE%20%D0%B4%D0%B8%D0%B0%D0%BF%D0%B0%D0%B7%D0%BE%D0%BD%D0%B0.jpg"
    photo_television = "https://www.krugosvet.ru/sites/krugosvet.ru/files/img01/1001215_6652_003.gif"
    # video = "https://youtu.be/9uWaZWBIBMg?t=1"

    album.attach_photo(photo=photo_optics, caption="Оптические частоты")
    album.attach_photo(photo=photo_television, caption="Виды частот")
    # album.attach_video(video=video)

    await message.answer_media_group(media=album)


@dp.message_handler(Text(contains="Articles", ignore_case=True) | Command(commands=["articles"]))
async def get_link_articles(message: types.Message):
    await message.reply(text='Встроенные <a href="https://telegra.ph/Vstroennye-filtry-v-aiogram-12-30">фильтры</a>'
                             ' в aiogram')
