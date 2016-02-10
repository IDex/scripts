#!/bin/env python3
import sys
import datetime as dt
import subprocess as sp
import time as t
import os
import re
import argparse
import collections

PROG = 'mpv'
FILE = os.path.expanduser('~/alarma.mp3')


class Alarm:

    def __init__(self, *args, repeat=True):
        for a in args:
            if 'h' not in a and 'm' not in a:
                self.rawtime = self.parse(
                    r'(?P<hours>[0-9]*)[:\.]*(?P<minutes>[0-9]*)', a)
                if self.rawtime:
                    break
        for a in args:
            self.rawdiff = self.parse(
                r'(?:(?P<hours>[0-9]*)h)*(?:(?P<minutes>[0-9]*)m)*', a)
            if self.rawdiff:
                break
        else:
            self.rawdiff = collections.defaultdict(int)
        self.time = None
        self.diff = None
        self.repeat = repeat
        self.setup()

    def setup(self):
        self.diff = dt.timedelta(
            hours=self._try_int(self.rawdiff.get('hours')),
            minutes=self._try_int(self.rawdiff.get('minutes'))
        )
        try:
            self.time = dt.datetime.combine(
                dt.datetime.today(),
                dt.time(
                    hour=self._try_int(self.rawtime.get('hours')),
                    minute=self._try_int(self.rawtime.get('minutes')))
            )
        except AttributeError:  # type is timer
            self.time = dt.datetime.now()
            self.diff *= -1
            self.repeat = not self.repeat
        self.time -= self.diff
        if self.time < dt.datetime.now():
            self.time += dt.timedelta(days=1)

    @staticmethod
    def parse(regex, string):
        m = re.search(regex, string)
        # making sure match object isn't full of None, i.e. not an actual match
        if m and {x for x in m.groupdict().values() if x is not None}:
            return m.groupdict(0)
        else:
            return None

    def start(self):
        print(
            'Given time: {}\n'
            'Alarm time: {}\n'
            'Repeat?: {}\n'
            'Original Delta: {}'
            .format(
                sys.argv[1:],
                str(self.time),
                bool(self.repeat),
                str(self.time - dt.datetime.now()).rsplit('.')[0]))
        try:
            self.run()
        except KeyboardInterrupt:
            pass
        return self

    @staticmethod
    def ring():
        sp.call(
            [PROG, FILE],
            stdout=sp.DEVNULL)
        t.sleep(3)

    def run(self):
        while True:
            diff = self.time - dt.datetime.now()
            if diff < dt.timedelta():
                self.ring()
                if self.repeat:
                    continue
                else:
                    break
            print('Delta: {}'.format(
                str(diff)).rsplit('.')[0], end='\r')
            t.sleep(3)

    @staticmethod
    def _try_int(s):
        try:
            s = int(s)
        except (TypeError, ValueError):
            return 0
        return s

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description='Ring alarm after set delta or at set time')
    p.add_argument('time', metavar='T',
                   help='Alarm time as hh:mm, hh.mm, h or m')
    p.add_argument('diff', nargs='?', default=0, metavar='D',
                   help='''How much earlier should the alarm ring?
                   If T is left out: After how much time should the alarm ring?
                   Enter as XXhXXm''')
    p.add_argument('-r', action='count', default=0,
                   help='''Toggle repeat, default depends on type of time''')
    pargs = p.parse_args()
    if not pargs.diff:
        Alarm(pargs.time, pargs.time, repeat=not pargs.r).start()
    else:
        Alarm(pargs.time, pargs.diff, repeat=not pargs.r).start()
