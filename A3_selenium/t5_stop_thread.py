# coding: utf-8
"""
@author: Evan
@time: 2020-01-10 18:02
"""
import time
import threading

import ctypes
import inspect


class StopThreading:
    """
    强制关闭线程的方法封装在StopThreading类中
    """
    @staticmethod
    def _async_raise(tid, exc_type):
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exc_type):
            exc_type = type(exc_type)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)


i = 1


def index_page():
    global i
    while True:
        time.sleep(1)
        if isinstance(i, int):
            i += 1

        print(i)
        if i == 8:
            i = 'exit'
            continue


# 尝试一个线程，死循环
threads = threading.Thread(target=index_page)
threads.start()


def thread_stop():
    global i
    while True:
        if i == 'exit':
            if threads:
                # threads.join()
                StopThreading().stop_thread(threads)
                i = 'quit'
                print(i)
                break


# 开启另外一个线程，强制终止上一个线程，并退出程序
thread_st = threading.Thread(target=thread_stop)
thread_st.start()




