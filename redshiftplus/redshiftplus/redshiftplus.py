#!/bin/env python3
import datetime as dt
import subprocess as sp
from time import sleep


class Timer:

    def __init__(self, start, stop, action, undo_action):
        self.start = [int(x) for x in start.split('.')]
        self.stop = [int(x) for x in stop.split('.')]
        self.action = action
        self.undo_action = undo_action
        self.done = False

    def do(self):
        if self.done:
            return
        sp.Popen(self.action.split())
        self.done = True

    def undo(self):
        if not self.done:
            return
        sp.Popen(self.undo_action.split())
        self.done = False

    def poll(self):
        if dt.datetime.now().time() > dt.time(*self.start) or dt.time(*self.stop) > dt.datetime.now().time():
            self.do()
        else:
            self.undo()


def main():
    start_time = '23.00'
    stop_time = '07.00'

    timer = Timer(start_time, stop_time,
                  'redshift -O 3400', 'redshift -x')

    try:
        while True:
            timer.poll()
            sleep(5)
    except KeyboardInterrupt:
        timer.undo()

if __name__ == '__main__':
    main()
