import datetime
import time

timeStamp = 1381419600

t = time.mktime(datetime.date.today().timetuple())
print(int(t))
print(type(timeStamp),type(t))
timeArray = time.localtime(int(t))
print(type(timeArray))
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
otherStyleTime1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
print(otherStyleTime)
print(otherStyleTime1)