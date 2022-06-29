import multiprocessing
import time

def func():

    pname = multiprocessing.current_process().name
    pid = multiprocessing.current_process().pid
    print(f"当前进程id{pid}, 进程名字{pname}")

    for i in range(5):
        print(pname, pid)
        time.sleep(1)

    pass


print(func())