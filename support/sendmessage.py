import smtplib
import os

# Добавляем необходимые подклассы - MIME-типы
# Multipurpose Internet Mail Extensions — многоцелевые расширения интернет-почты, стандарт, описывающий передачу
# различных типов данных по электронной почте, а также, в общем случае, спецификация для кодирования информации и
# форматирования сообщений таким образом, чтобы их можно было пересылать по Интернету.
import mimetypes  # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders                                  # Импортируем энкодер
from email.mime.base import MIMEBase                        # Общий тип
from email.mime.text import MIMEText                        # Текст/HTML
from email.mime.image import MIMEImage                      # Изображения
from email.mime.audio import MIMEAudio                      # Аудио
from email.mime.multipart import MIMEMultipart              # Многокомпонентный объект


mail_from = 'deltacentr24@gmail.com'
mail_to = 'deltacentr06@mail.ru'
password = '93l7Non2aJMQ'

filepath = "../documents/list_schedule.xlsx"
basename = os.path.basename(filepath)
filesize = os.path.getsize(filepath)
print(f"Название {basename}")
print(f"Размер {filesize}")

ctype, encoding = mimetypes.guess_type(filepath)
# print(ctype, encoding)
maintype, subtype = ctype.split('/', 1)
# print(maintype, subtype)

# print(os.path.isfile("../documents"))
# print(os.path.exists(filepath))

dir = os.listdir("../documents")
for file in dir:
    print(file)

msg = MIMEMultipart()  # Создаем сообщение
msg['From'] = mail_from  # Адресат
msg['To'] = mail_to  # Получатель
msg['Subject'] = 'Тема сообщения передачи'  # Тема сообщения

body = 'Полученное сообщения'  # Текст сообщения
msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
file.set_payload(open(filepath, 'rb').read())  # Добавляем содержимое общего типа (полезную нагрузку)
encoders.encode_base64(file)

file.add_header('Content-Disposition', 'attachment', filename=basename) # Добавляем заголовки
msg.attach(file)                                        # Присоединяем файл к сообщению

# server = smtplib.SMTP('smtp.gmail.com: 587')
# server.starttls()
# server.login(mail_from, password)
# server.sendmail(mail_from, mail_to, msg.as_string())
# server.quit()
