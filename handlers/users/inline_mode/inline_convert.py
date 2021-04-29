from aiogram import types
import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.types import InputFile
import math
from aiogram.utils.markdown import hbold, hcode, hitalic, hunderline, hstrikethrough, hlink
import datetime

from data.config import allowed_users
from data.party_day import group_day
from loader import dp, bot, db


@dp.inline_handler()
async def empty_query(query: types.InlineQuery):
    print(query.from_user.values)
    print(query.values['query'])

    user = db.select_user(id=query.from_user.id)

    if user == None:
        await query.answer(
            results=[],
            switch_pm_text="Бот недоступен. Подключить бота",
            switch_pm_parameter="connect_user",
            cache_time=5)
        return

    # Обработка команды перевода в дБ
    if re.match(r"convert\s?\d+", query.values['query']):

        result = re.findall(r'\d+', query.values['query'])

        if len(result) == 1:

            dbm = 10 * math.log10(int(result[0]) / 0.001)
            db_power = 10 * math.log10(int(result[0]))
            db_voltage = 20 * math.log10(int(result[0]))
            print(dbm)
            bell = db_power / 10

            await query.answer(
                results=[
                    types.InlineQueryResultArticle(
                        id="1",
                        title="Результаты",
                        input_message_content=types.InputTextMessageContent(
                            message_text=f"<b>Выполнение</b>\n"
                                         f"Элемент <b>{result[0]}</b>\n"
                                         f"{dbm:.5f} dBm\n"
                                         f"{db_power:.5f} dB по мощности\n"
                                         f"{db_voltage:.5f} dB по напряжению\n"
                                         f"{bell:.5f} в Беллах",
                            parse_mode="HTML"
                        ),
                        description=f"{dbm} dBm\n"
                                    f"{db_power} dB по мощности\n"
                                    f"{db_voltage} dB по напряжению"
                    ),
                ],
                cache_time=5)

        elif len(result) == 2:
            Np = math.log(int(result[0]) / int(result[1]))
            await query.answer(
                results=[
                    types.InlineQueryResultArticle(
                        id="1",
                        title="Результаты",
                        input_message_content=types.InputTextMessageContent(
                            message_text=f"<b>Выполнение</b>\n"
                                         f"Элементы <b>{result[0]}</b> и <b>{result[1]}</b>\n"
                                         f"Отношение двух величин: {Np:.5f} непер",
                            parse_mode="HTML"
                        ),
                        description=f"Отношение двух величин: {Np:.5f} непер"
                    ),
                ],
                cache_time=5)

        else:
            await query.answer(
                results=[
                    types.InlineQueryResultArticle(
                        id="1",
                        title="Результаты",
                        input_message_content=types.InputTextMessageContent(
                            message_text=f"<b>Перебор элементов перебора</b>\n",
                            parse_mode="HTML"
                        ),
                        description=f"Для перевода долно быть от одного до двух элементов"
                    ),
                ],
                cache_time=5)

    # Обработка команды перевода по мощности и амплитуде
    elif re.match(r"(cnt)?\s?[+-]?([0-9]*[.,])?[0-9]+[VvWwВвТт]", query.values['query']):

        if query.values['query'][-1] in ['V', 'v', 'В', 'в']:
            result = re.findall(r'[+-]?([0-9]+([.,]\d+)?)', query.values['query'])
            result = float(result[0][0].replace(',', '.'))
            # print(result)
            dBV = 20 * math.log10(result)
            dBmcV = dBV + 120
            dBmW = dBmcV - 90 - 10 * math.log10(50)
            dBW = dBmW - 30
            time = datetime.datetime.now()
            await query.answer(
                results=[
                    types.InlineQueryResultArticle(
                        id="1",
                        title="Результаты",
                        input_message_content=types.InputTextMessageContent(
                            message_text=f"<b>Отношение амплитуд</b>\n"
                                         f"<u>{result} В, вольт</u>\n"
                                         f"<code>{dBV:.5f}</code> <i>dBV, децибел-вольт</i>\n"
                                         f"<code>{dBmcV:.5f}</code> <i>дБмкВ, децибел-микровольт</i>\n"
                                         f"\n"
                                         f"Преобразование дБмкВ в дБмВт\n"
                                         f"<code>{dBmW:.5f}</code> <i>дБмВт, децибел-милливатт</i>\n"
                                         f"<code>{dBW:.5f}</code> <i>дБВт, децибел-ватт</i>\n"
                                         f"<pre>{time.hour} : {time.minute}   ({time.date()})</pre>",
                            parse_mode="HTML"
                        ),
                        description=f"Отношение напряжений относительно одного вольта или микровольта.\n"
                                    f"{dBV:.5f} dBV, децибел-вольт\n"
                    ),
                ],
                cache_time=5)

        else:
            result = re.findall(r'[+-]?([0-9]+([.,]\d+)?)', query.values['query'])
            result = float(result[0][0].replace(',', '.'))
            dBW = 10 * math.log10(result)
            dBmW = dBW + 30
            dBmW_in_dBmcB = dBmW + 90 + 10 * math.log10(50)
            dBV = dBmW_in_dBmcB - 120
            time = datetime.datetime.now()
            await query.answer(
                results=[
                    types.InlineQueryResultArticle(
                        id="1",
                        title="Результаты",
                        input_message_content=types.InputTextMessageContent(
                            message_text=f"<b>Децибел по мощности</b>\n"
                                         f"<u>{result} Вт, ватт</u>\n"
                                         f"<code>{dBW:.5f}</code> <i>дБВт, децибел-ватт</i>\n"
                                         f"<code>{dBmW:.5f}</code> <i>дБмВт, децибел-милливатт</i>\n"
                                         f"\n"
                                         f"Преобразование дБмВт в дБмкВ\n"
                                         f"<code>{dBmW_in_dBmcB:.5f}</code> <i>дБмкВ, децибел-микровольт</i>\n"
                                         f"<code>{dBV:.5f}</code> <i>дБВ, децибел-вольт</i>\n"
                                         f"<pre>{time.hour} : {time.minute}   ({time.date()})</pre>",
                            parse_mode="HTML"
                        ),
                        description=f"Отношение мощностей относительно одного ватта или милливатта.\n"
                                    f"{dBW:.5f} дБВт, децибел-ватт\n"
                    ),
                ],
                cache_time=5)

    # Обработка команды выводящей рассписание
    elif re.match(r"(sche(dule)?\s?(\d+)?)|(рас(писание)?\s?(\d+)?)", query.values['query'].lower()):
        number_party = re.findall(r'\d+', query.values['query'])
        if number_party == []:
            user = db.select_user(id=query.from_user.id)
            if user[3] is not None:
                number_party = [str(user[3])]
            else:
                await query.answer(
                    results=[],
                    switch_pm_text="Бот недоступен. Укажите группу",
                    switch_pm_parameter="number_party",
                    cache_time=5)
                return

        number_day = int(datetime.datetime.now().isoweekday()) + 1
        print(number_party)

        if number_day in [7, ]:
            await query.answer(
                results=[
                    types.InlineQueryResultArticle(
                        id="1",
                        title="Завтра нет занятий",
                        input_message_content=types.InputTextMessageContent(
                            message_text=f"<b>Завтра нет занятий</b>\n",
                            parse_mode="HTML"
                        )
                    ),
                ],
                cache_time=5)
            return

        await query.answer(
            results=[
                types.InlineQueryResultCachedPhoto(
                    id='1',
                    photo_file_id=group_day[number_party[0]][number_day][1],
                    description=group_day[number_party[0]][number_day][0],
                    caption=f'Рассписание на {group_day[number_party[0]][number_day][0].lower()}',
                    title=group_day[number_party[0]][number_day][0]
                )
            ]
        )

    else:
        await query.answer(
            results=[],
            switch_pm_text="Перейти в бота",
            switch_pm_parameter="connect_bot",
            cache_time=5)
        return
