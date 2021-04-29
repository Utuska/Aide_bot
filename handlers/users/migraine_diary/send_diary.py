import os.path
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from aiogram.dispatcher.filters import Command
from aiogram import types
from loader import dp, bot, db


# @dp.message_handler(Command("open"))
# async def update_email(message: types.Message, state: FSMContext):
#     records = db.select_record(id_recording=521804630)
#     status = []
#     for item in records:
#         status.append(item[3])
#     await message.answer("Показ записей базы")


def formation_excel(records, filename):
    date = []
    status = []
    for item in records:
        status.append(item[3])
        date.append(item[2])

    import pandas as pd
    from openpyxl import load_workbook

    df = pd.DataFrame({'Date': date,
                       'Status': status
                       })

    abspath = os.path.abspath('documents/')
    filepath = f'{abspath}/{filename}.xlsx'
    df.to_excel(filepath)


# Команда отправки сообщений на почту
@dp.message_handler(Command("send"))
async def update_email(message: types.Message, state: FSMContext):
    # get user data from db
    user = db.select_user(id=message.from_user.id)
    email = user[2]
    records = db.select_record(id_recording=message.from_user.id)

    import os
    from translate import Translator

    # translate user name
    name_user = message.from_user.last_name
    translator = Translator(from_lang="ru", to_lang="en")
    filename = translator.translate(name_user)
    # file formation function
    formation_excel(records, filename)

    abspath = os.path.abspath('documents/')
    filepath = f'{abspath}/{filename}.xlsx'

    # check, if the user's mail is specified
    if email is None:
        await message.answer("Укажи свою почту, на которую будет отправлен файл (команда /mail)")
        document_link = InputFile(f'documents/{filename}.xlsx')
        await message.answer_document(document=document_link, caption="Дневник заметок по мигрени")

    # Добавляем необходимые подклассы - MIME-типы
    # Multipurpose Internet Mail Extensions — многоцелевые расширения интернет-почты, стандарт, описывающий передачу
    # различных типов данных по электронной почте, а также, в общем случае, спецификация для кодирования информации и
    # форматирования сообщений таким образом, чтобы их можно было пересылать по Интернету.
    import mimetypes  # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
    from email import encoders  # Импортируем энкодер
    from email.mime.base import MIMEBase  # Общий тип
    from email.mime.text import MIMEText  # Текст/HTML
    from email.mime.image import MIMEImage  # Изображения
    from email.mime.audio import MIMEAudio  # Аудио
    from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
    import smtplib

    mail_from = 'deltacentr24@gmail.com'
    mail_to = email
    password = '93l7Non2aJMQ'

    basename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    # print(f"Название {basename}")
    # print(f"Размер {filesize}")
    ctype, encoding = mimetypes.guess_type(filepath)
    maintype, subtype = ctype.split('/', 1)
    print(maintype, subtype)

    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = mail_from  # Адресат
    msg['To'] = mail_to  # Получатель
    msg['Subject'] = 'Записи дневника'  # Тема сообщения

    body = 'Отправлен дневник от бота'  # Текст сообщения
    msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

    file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
    file.set_payload(open(filepath, 'rb').read())  # Добавляем содержимое общего типа (полезную нагрузку)
    encoders.encode_base64(file)

    file.add_header('Content-Disposition', 'attachment', filename=basename)  # Добавляем заголовки
    msg.attach(file)  # Присоединяем файл к сообщению

    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(mail_from, password)
    server.sendmail(mail_from, mail_to, msg.as_string())
    server.quit()

    await message.answer(f"Данные отправлены на вашу почту ({email})")
