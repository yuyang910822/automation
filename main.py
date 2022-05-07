import time,datetime

print(int(time.mktime(datetime.date.today().timetuple())*1000))
yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
print(yesterday)