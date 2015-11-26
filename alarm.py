#!/bin/env python3
import sys
import datetime as dt
import subprocess as sp
import time as t
import os
import argparse

PROG = 'mpv'
FILE = os.path.expanduser('~/alarma.mp3')


def normalAlarm(time, diff):
    '''Alarm that rings at certain time'''
    formattedtime = dt.time(*(int(x) for x in time.split(':')))
    today = dt.datetime.today()
    atime = dt.datetime.combine(today, formattedtime)
    atime = atime - dt.timedelta(days=0, hours=diff)
    if dt.datetime.now() > atime:
        atime += dt.timedelta(days=1)
    return (atime, atime - dt.datetime.now())


def timerAlarm(time, x, mult):
    '''Alarm that rings after certain time'''
    cleantime = time.rstrip(x)
    diff = dt.timedelta(minutes=int(cleantime) * mult)
    return (dt.datetime.now() + diff, diff)


def makeAlarm(timearg, diff=0, repeat=0):
    once = not repeat
    if 'm' in timearg:
        atime, dtime = timerAlarm(timearg, 'm', 1)
    elif 'h' in timearg:
        atime, dtime = timerAlarm(timearg, 'h', 60)
    else:
        atime, dtime = normalAlarm(timearg, diff)
        once = not once

    print("""\
Given time: {}
Alarm time: {}
Repeat?: {}
Original Delta: {}\
""".format(sys.argv[1], str(atime).rsplit('.')[0], not once,
           str(dtime).rsplit('.')[0]))

    try:
        while True:
            diff = dt.datetime.now() > atime and atime < dt.datetime.now() + \
                dt.timedelta(days=0, hours=0, minutes=10)
            if diff:
                sp.call(
                    [PROG, FILE],
                    stdout=sp.DEVNULL)
                t.sleep(3)
                if once or args.r > 1:
                    if args.r > 1:
                        args.r -= 2
                        makeAlarm(args)
                    break
                else:
                    continue
            print('Delta: {}'.format(
                str(atime - dt.datetime.now())).rsplit('.')[0], end='\r')
            t.sleep(3)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description='Ring alarm after set delta or at set time')
    p.add_argument('time', metavar='T',
                   help='Alarm time, alarm: hh:mm, h; timer: xm, xh')
    p.add_argument('diff', nargs='?', default=0, metavar='D', type=int,
                   help='How many hours earlier should the alarm ring')
    p.add_argument('-r', action='count', default=0,
                   help='''Toggle repeat, default depends on type of time''')
    args = p.parse_args()
    makeAlarm(args.time, args.diff, args.r)
