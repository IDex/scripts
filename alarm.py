import sys
import datetime as dt
import subprocess as sp
import time as t
import os


def normalAlarm():
    time = dt.time(*args)
    today = dt.datetime.today()
    atime = dt.datetime.combine(today, time)
    try:
        diff = sys.argv[2]
        atime = atime - dt.timedelta(days=0, hours=int(diff))
    except:
        pass
    if dt.datetime.now() > atime:
        atime += dt.timedelta(days=1)
    return atime


def timerAlarm(x, mult):
    args = sys.argv[1].rstrip(x)
    return dt.datetime.now() + dt.timedelta(minutes=int(args)*mult)

try:
    args = [int(a) for a in sys.argv[1].split(':')]
except:
    if sys.argv[1] == 'h':
        print(
            """

ex.
    alarm 10:00 8
        -> alarm at 02:00
    alarm 01:00
        -> alarm at 01:00
    alarm 5m
        -> alarm 5min from now on
    alarm 5m r
        -> repeat the alarm
""")
        raise SystemExit
once = True
try:
    if sys.argv[2] == 'r':
        once = False
except:
    pass
if 'm' in sys.argv[1]:
    atime = timerAlarm('m', 1)
elif 'h' in sys.argv[1]:
    atime = timerAlarm('h', 60)
else:
    atime = normalAlarm()
    once = False
print("""\
Given time: {}
Alarm time: {}
Repeat?: {}\
""".format(sys.argv[1], atime, not once))
while True:
    diff = dt.datetime.now() > atime
    if diff:
        sp.call(['mpv', os.path.expanduser('~/alarma.mp3')])
        t.sleep(5)
        if once:
            break
        else:
            continue
    t.sleep(5)
