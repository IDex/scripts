import sys, datetime as dt, subprocess as sp
import os
import time as t

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
""")
        raise SystemExit

print(sys.argv[1])
def normalAlarm():
    time = dt.time(*args)
    today = dt.datetime.today()
    atime = dt.datetime.combine(today, time)
    try:
        diff = sys.argv[2]
        atime = atime - dt.timedelta(days=0, hours = int(diff))
    except:
        pass
    if dt.datetime.now() > atime:
        atime += dt.timedelta(days=1)
    return atime

def TimerAlarm(x, mult):
    args = sys.argv[1].rstrip(x)
    return dt.datetime.now() + dt.timedelta(minutes=int(args)*mult)

if 'm' in sys.argv[1]:
    atime = TimerAlarm('m',1)
elif 'h' in sys.argv[1]:
    atime = TimerAlarm('h',60)
else:
    atime = normalAlarm()
print(atime)
while True:
    diff = dt.datetime.now() > atime
    if diff:
        sp.call(['mpv',os.path.expanduser('~/alarma.mp3')])
        t.sleep(5)
        #break
        continue
    t.sleep(5)
