import time



time_str = "2022-03-18 10:54:00"
time_stamp = time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))
print(time_stamp)