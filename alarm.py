import sys
import datetime as dt
import subprocess as sp
import time as t
import os
import argparse

p = argparse.ArgumentParser(
    description='Ring alarm after set delta or at set time')
# ex.
#    alarm 10:00 8
#        -> alarm at 02:00, repeat
#    alarm 1
#        -> alarm at 01:00, repeat
#    alarm 5m
#        -> alarm 5min from now on, don't repeat
#    alarm 5m -r
#        -> repeat the alarm
#''')
p.add_argument('time', metavar='T',
               help='Alarm time, alarm: hh:mm, h; timer: xm, xh')
p.add_argument('diff', nargs='?', default=0, metavar='D', type=int,
               help='How many hours earlier should the alarm ring')
p.add_argument('-r', action='store_true', default=False,
               help='''Toggle repeat, default depends on type of time''')
args = p.parse_args()


def normalAlarm(time, diff):
    formattedtime = dt.time(*(int(x) for x in time.split(':')))
    today = dt.datetime.today()
    atime = dt.datetime.combine(today, formattedtime)
    atime = atime - dt.timedelta(days=0, hours=diff)
    if dt.datetime.now() > atime:
        atime += dt.timedelta(days=1)
    return (atime, atime - dt.datetime.now())


def timerAlarm(time, x, mult):
    cleantime = time.rstrip(x)
    diff = dt.timedelta(minutes=int(cleantime) * mult)
    return (dt.datetime.now() + diff, diff)

once = not args.r
if 'm' in args.time:
    atime, dtime = timerAlarm(args.time, 'm', 1)
elif 'h' in args.time:
    atime, dtime = timerAlarm(args.time, 'h', 60)
else:
    atime, dtime = normalAlarm(args.time, args.diff)
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
        diff = dt.datetime.now() > atime
        if diff:
            sp.call(
                ['mpv', os.path.expanduser('~/alarma.mp3')], stdout=sp.DEVNULL)
            t.sleep(5)
            if once:
                break
            else:
                continue
        print('Delta: {}'.format(
            str(atime - dt.datetime.now())).rsplit('.')[0], end='\r')
        t.sleep(5)
except KeyboardInterrupt:
    pass
