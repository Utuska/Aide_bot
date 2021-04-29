import datetime


timezone = datetime.tzinfo()
print(timezone)


offset = datetime.timedelta(hours=3)
timezone = datetime.timezone(offset, name='MСК')
print(timezone)


import pytz

moscow_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
print(moscow_time.date())
print(pytz.timezone('Europe/Moscow'))