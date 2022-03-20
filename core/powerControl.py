import threading
import time
import ctypes

EXIT_FLAG = False
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002
ES_AWAYMODE_REQUIRED = 0x00000040
ES_CONTINUOUS = 0x80000000


def timer_action(wait_time):
    count = wait_time
    while True:
        if EXIT_FLAG:
            break
        if count >= wait_time:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_DISPLAY_REQUIRED)
            count = 0
        count = count + 1
        time.sleep(1)


def start_timer():
    global EXIT_FLAG
    EXIT_FLAG = False
    t1 = threading.Thread(target=timer_action, args=(60,))
    t1.start()


def end_timer():
    global EXIT_FLAG
    EXIT_FLAG = True
