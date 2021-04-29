# from aiogram import types
# import re
#
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Command, CommandStart
# from aiogram.types import InputFile
# import math
# from aiogram.utils.markdown import hbold, hcode, hitalic, hunderline, hstrikethrough, hlink
# import datetime
#
# from data.config import allowed_users
# from data.party_day import group_day
# from loader import dp, bot, db
#
#
# @dp.inline_handler(text="")
# async def empty_query(query: types.InlineQuery):
#     await query.answer(
#         results=[
#             types.InlineQueryResultArticle(
#                 id="unknown",
#                 title="Введите запрос",
#                 input_message_content=types.InputTextMessageContent(
#                     message_text="Не обязательно жать при этом на кнопку",
#                     parse_mode="HTML",
#                 ),
#                 description="Команда 'convert <digit>' - переведет число в разные системы счисления",
#             ),
#         ],
#
#         cache_time=5)
#
#
# @dp.inline_handler()
# async def empty_query(query: types.InlineQuery):
#     print(query.from_user.values)
#     print(query.values['query'])
#
#     user = db.select_user(id=query.from_user.id)
#
#     if user == None:
#         await query.answer(
#             results=[],
#             switch_pm_text="Бот недоступен. Подключить бота",
#             switch_pm_parameter="connect_user",
#             cache_time=5)
#         return
#
#     if re.match(r"convert\s?\d+", query.values['query']):
#
#         result = re.findall(r'\d+', query.values['query'])
#
#         if len(result) == 1:
#
#             dbm = 10 * math.log10(int(result[0]) / 0.001)
#             db_power = 10 * math.log10(int(result[0]))
#             db_voltage = 20 * math.log10(int(result[0]))
#             print(dbm)
#             bell = db_power / 10
#
#             await query.answer(
#                 results=[
#                     types.InlineQueryResultArticle(
#                         id="1",
#                         title="Результаты",
#                         input_message_content=types.InputTextMessageContent(
#                             message_text=f"<b>Выполнение</b>\n"
#                                          f"Элемент <b>{result[0]}</b>\n"
#                                          f"{dbm:.5f} dBm\n"
#                                          f"{db_power:.5f} dB по мощности\n"
#                                          f"{db_voltage:.5f} dB по напряжению\n"
#                                          f"{bell:.5f} в Беллах",
#                             parse_mode="HTML"
#                         ),
#                         description=f"{dbm} dBm\n"
#                                     f"{db_power} dB по мощности\n"
#                                     f"{db_voltage} dB по напряжению"
#                     ),
#                 ],
#                 cache_time=5)
#
#         elif len(result) == 2:
#             Np = math.log(int(result[0]) / int(result[1]))
#             await query.answer(
#                 results=[
#                     types.InlineQueryResultArticle(
#                         id="1",
#                         title="Результаты",
#                         input_message_content=types.InputTextMessageContent(
#                             message_text=f"<b>Выполнение</b>\n"
#                                          f"Элементы <b>{result[0]}</b> и <b>{result[1]}</b>\n"
#                                          f"Отношение двух величин: {Np:.5f} непер",
#                             parse_mode="HTML"
#                         ),
#                         description=f"Отношение двух величин: {Np:.5f} непер"
#                     ),
#                 ],
#                 cache_time=5)
#
#         else:
#             await query.answer(
#                 results=[
#                     types.InlineQueryResultArticle(
#                         id="1",
#                         title="Результаты",
#                         input_message_content=types.InputTextMessageContent(
#                             message_text=f"<b>Перебор элементов перебора</b>\n",
#                             parse_mode="HTML"
#                         ),
#                         description=f"Для перевода долно быть от одного до двух элементов"
#                     ),
#                 ],
#                 cache_time=5)
#
#     elif re.match(r"(cnt)?\s?[+-]?([0-9]*[.,])?[0-9]+[VvWwВвТт]", query.values['query']):
#
#         if query.values['query'][-1] in ['V', 'v', 'В', 'в']:
#             result = re.findall(r'[+-]?([0-9]+([.,]\d+)?)', query.values['query'])
#             result = float(result[0][0].replace(',', '.'))
#             print(result)
#             dBV = 20 * math.log10(result)
#             dBmcV = dBV + 120
#             dBmW = dBmcV - 90 - 10 * math.log10(50)
#             dBW = dBmW - 30
#             time = datetime.datetime.now()
#             await query.answer(
#                 results=[
#                     types.InlineQueryResultArticle(
#                         id="1",
#                         title="Результаты",
#                         input_message_content=types.InputTextMessageContent(
#                             message_text=f"<b>Отношение амплитуд</b>\n"
#                                          f"<u>{result} В, вольт</u>\n"
#                                          f"<code>{dBV:.5f}</code> <i>dBV, децибел-вольт</i>\n"
#                                          f"<code>{dBmcV:.5f}</code> <i>дБмкВ, децибел-микровольт</i>\n"
#                                          f"\n"
#                                          f"Преобразование дБмкВ в дБмВт\n"
#                                          f"<code>{dBmW:.5f}</code> <i>дБмВт, децибел-милливатт</i>\n"
#                                          f"<code>{dBW:.5f}</code> <i>дБВт, децибел-ватт</i>\n"
#                                          f"<pre>{time.hour} : {time.minute}   ({time.date()})</pre>",
#                             parse_mode="HTML"
#                         ),
#                         description=f"Отношение напряжений относительно одного вольта или микровольта.\n"
#                                     f"{dBV:.5f} dBV, децибел-вольт\n"
#                     ),
#                 ],
#                 cache_time=5)
#
#         else:
#             result = re.findall(r'[+-]?([0-9]+([.,]\d+)?)', query.values['query'])
#             result = float(result[0][0].replace(',', '.'))
#             dBW = 10 * math.log10(result)
#             dBmW = dBW + 30
#             dBmW_in_dBmcB = dBmW + 90 + 10 * math.log10(50)
#             dBV = dBmW_in_dBmcB - 120
#             time = datetime.datetime.now()
#             await query.answer(
#                 results=[
#                     types.InlineQueryResultArticle(
#                         id="1",
#                         title="Результаты",
#                         input_message_content=types.InputTextMessageContent(
#                             message_text=f"<b>Децибел по мощности</b>\n"
#                                          f"<u>{result} Вт, ватт</u>\n"
#                                          f"<code>{dBW:.5f}</code> <i>дБВт, децибел-ватт</i>\n"
#                                          f"<code>{dBmW:.5f}</code> <i>дБмВт, децибел-милливатт</i>\n"
#                                          f"\n"
#                                          f"Преобразование дБмВт в дБмкВ\n"
#                                          f"<code>{dBmW_in_dBmcB:.5f}</code> <i>дБмкВ, децибел-микровольт</i>\n"
#                                          f"<code>{dBV:.5f}</code> <i>дБВ, децибел-вольт</i>\n"
#                                          f"<pre>{time.hour} : {time.minute}   ({time.date()})</pre>",
#                             parse_mode="HTML"
#                         ),
#                         description=f"Отношение мощностей относительно одного ватта или милливатта.\n"
#                                     f"{dBW:.5f} дБВт, децибел-ватт\n"
#                     ),
#                 ],
#                 cache_time=5)
#
#     elif re.match(r"(sche(dule)?\s?(\d+)?)|(рас(писание)?\s?(\d+)?)", query.values['query'].lower()):
#         number_party = re.findall(r'\d+', query.values['query'])
#         if number_party == []:
#             user = db.select_user(id=query.from_user.id)
#             if user[3] is not None:
#                 number_party = [str(user[3])]
#             else:
#                 await query.answer(
#                     results=[],
#                     switch_pm_text="Бот недоступен. Укажите группу",
#                     switch_pm_parameter="number_party",
#                     cache_time=5)
#                 return
#
#         number_day = int(datetime.datetime.now().isoweekday()) + 1
#         print(number_party)
#
#         if number_day in [7, ]:
#             await query.answer(
#                 results=[
#                     types.InlineQueryResultArticle(
#                         id="1",
#                         title="Завтра нет занятий",
#                         input_message_content=types.InputTextMessageContent(
#                             message_text=f"<b>Завтра нет занятий</b>\n",
#                             parse_mode="HTML"
#                         )
#                     ),
#                 ],
#                 cache_time=5)
#             return
#
#         await query.answer(
#             results=[
#                 types.InlineQueryResultCachedPhoto(
#                     id='1',
#                     photo_file_id=group_day[number_party[0]][number_day][1],
#                     description=group_day[number_party[0]][number_day][0],
#                     caption=f'Рассписание на {group_day[number_party[0]][number_day][0].lower()}',
#                     title=group_day[number_party[0]][number_day][0]
#                 )
#             ]
#         )
#
#     # if re.match(r"\d\d\d", query.values['query']) and len(query.values['query']) == 3:
#     #     print("Выполнение")
#     #     await query.answer(
#     #         results=[
#     #             types.InlineQueryResultArticle(
#     #                 id="1",
#     #                 title=f"{query.values['query']}",
#     #                 input_message_content=types.InputTextMessageContent(
#     #                     message_text=f"Ваше число {query.values['query']}",
#     #                     parse_mode="HTML"
#     #                 ),
#     #                 url="https://core.telegram.org/bots/api#inlinequeryresult",
#     #                 thumb_url="https://apps-cdn.athom.com/app/org.telegram.api.bot/1/1c9f8d07-be07-442d-933d-16fd212a68f1/assets/images/large.png",
#     #                 description="Описание, в инлнайн режиме"
#     #             )
#     #         ]
#     #     )
#     # await query.answer(
#     #     results=[
#     #         types.InlineQueryResultPhoto(
#     #             id="2",
#     #             description="Таблица переводов величин",
#     #             photo_url="https://st2.depositphotos.com/4285045/7260/i/600/depositphotos_72609979-stock-photo-ojos-de-gata.jpg",
#     #             thumb_url="https://st2.depositphotos.com/4285045/7260/i/600/depositphotos_72609979-stock-photo-ojos-de-gata.jpg",
#     #             title="Таблица перевода",
#     #             caption="Перевод"
#     #         )
#     #     ]
#     # )
#     # await query.answer(
#     #     results=[
#     #         types.InlineQueryResultArticle(
#     #             id="unknown",
#     #             title=f"{query.from_user.values}",
#     #             input_message_content=types.InputTextMessageContent(
#     #                 message_text="<b>Выполнение</b>",
#     #                 parse_mode="HTML"
#     #             ),
#     #         ),
#     #     ],
#     #
#     #     cache_time=5)
#
#
# # @dp.inline_handler()
# # async def empty_query(query: types.InlineQuery):
# #     user = db.select_user(id=query.from_user.id)
# #     print(user)
# #     # if user[0] not in allowed_users:
# #     if user == None:
# #         await query.answer(
# #             results=[],
# #             switch_pm_text="Бот недоступен. Подключить бота",
# #             switch_pm_parameter="connect_user",
# #             cache_time=5)
# #         return
# #     await query.answer(
# #         results=[
# #             types.InlineQueryResultArticle(
# #                 id="1",
# #                 title="Название, которое отображается в инлайн режиме!",
# #                 input_message_content=types.InputTextMessageContent(
# #                     message_text="Тут какой-то <b>текст</b>, который будет отправлен при нажатии на кнопку",
# #                     parse_mode="HTML"
# #                 ),
# #                 url="https://core.telegram.org/bots/api#inlinequeryresult",
# #                 thumb_url="https://apps-cdn.athom.com/app/org.telegram.api.bot/1/1c9f8d07-be07-442d-933d-16fd212a68f1/assets/images/large.png",
# #                 description="Описание, в инлнайн режиме"
# #             ),
# # types.InlineQueryResultCachedPhoto(
# #     id="2",
# #     photo_file_id="AgACAgIAAxkBAAICcV6jF5kAARvDMn99PQuVe9fBg-TKcAACQ64xG0WQGEm4F3v9dsbAAg7Hwg8ABAEAAwIAA3kAA9c_BgABGQQ",
# #     description="Описание, которое нигде не отображается!",
# #     caption="Тут будет подпись, которая отправится с картинкой, если на нее нажать",
# # ),
# #         types.InlineQueryResultVideo(
# #             id="4",
# #             video_url="https://pixabay.com/en/videos/download/video-10737_medium.mp4",
# #             caption="Подпись к видео",
# #             description="Какое-то описание",
# #             title="Название видео",
# #             thumb_url="https://i0.wp.com/globaldiversitypractice.com/wp-content/uploads/2018/11/asda.jpg",
# #             mime_type="video/mp4",  # Или video/mp4 text/html
# #         ),
# #     ],
# # )
#
#
# @dp.message_handler(CommandStart(deep_link="connect_user"))
# async def connect_user(message: types.Message):
#     db.add_user(message.from_user.id, message.from_user.full_name)
#     await message.answer("Вы подключены")
#
#
# @dp.message_handler(content_types=types.ContentType.PHOTO)
# async def get_file_id_p(message: types.Message):
#     await message.reply(message.photo[-1].file_id)
#
#
# @dp.message_handler(CommandStart(deep_link="number_party"))
# @dp.message_handler(Command("party"))
# async def update_email(message: types.Message, state: FSMContext):
#     await message.answer("Пришли мне свою группу")
#     await state.set_state("number_party")
#
#
# @dp.message_handler(state="number_party")
# async def enter_email(message: types.Message, state: FSMContext):
#     number_party = int(message.text)
#     db.update_number_party(number_party=number_party, id=message.from_user.id)
#     user = db.select_user(id=message.from_user.id)
#     await message.answer(f"Данные обновлены. Запись в БД: {user}")
#     await state.finish()
#
#
# @dp.message_handler(Command("frequency") | Command("частота"))
# async def send_table(message: types.Message):
#     photo_link = InputFile('photos/data.png')
#
#     await message.answer_photo(photo=photo_link, caption='Посмотреть полную информацию /all')
#
#
# @dp.message_handler(Command("all"))
# async def send_all(message: types.Message):
#     # Создаем альбом
#     album = types.MediaGroup()
#
#     photo_optics = "https://fibertop.ru/image/%D1%82%D1%80%D0%B0%D1%81%D1%81%D0%BE%D0%B8%D1%81%D0%BA%D0%B0%D1%82%D0%B5%D0%BB%D0%B8/fibertop_articles/%20%D0%BE%D0%BF%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B3%D0%BE%20%D0%B4%D0%B8%D0%B0%D0%BF%D0%B0%D0%B7%D0%BE%D0%BD%D0%B0.jpg"
#     photo_television = "https://www.krugosvet.ru/sites/krugosvet.ru/files/img01/1001215_6652_003.gif"
#     #video = "https://youtu.be/9uWaZWBIBMg?t=1"
#
#     album.attach_photo(photo=photo_optics, caption="Оптические частоты")
#     album.attach_photo(photo=photo_television, caption="Виды частот")
#     #album.attach_video(video=video)
#
#     await message.answer_media_group(media=album)