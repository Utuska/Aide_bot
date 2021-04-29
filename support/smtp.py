import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

password = '93l7Non2aJMQ'
my_email = 'deltacentr24@gmail.com'
to_email = 'deltacentr06@mail.ru'

filepath = "../documents/list_schedule.xlsx"
basename = os.path.basename(filepath)
filesize = os.path.getsize(filepath)
print(f"Название {basename}")
print(f"Размер {filesize}")

msg = MIMEMultipart()
message = 'Отправленное сообщпение'


msg.attach(MIMEText(message, 'plain'))

server = smtplib.SMTP('smtp.gmail.com: 587')
server.starttls()
server.login(my_email, password)
server.sendmail(my_email, to_email, msg.as_string())
server.quit()


# smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
# smtpObj.starttls()
# smtpObj.login('deltacentr24@gmail.com', '93l7Non2aJMQ')
# smtpObj.sendmail("deltacentr24@gmail.com", "deltacentr06@mail.ru","go to bed!")
# smtpObj.quit()