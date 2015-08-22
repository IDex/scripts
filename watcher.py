import os
import sys
import re
import json
import atexit
import subprocess as sp


def save():
    with open('watched.json', 'w') as f:
        json.dump(watched, f)

atexit.register(save)
wdir = os.path.expanduser('~/new/')
arg = sys.argv[1]
watched = []
try:
    with open('watched.json', 'r') as f:
        watched = json.load(f)
except:
    watched = []
matches = [x for x in os.listdir(wdir)
           if re.search(arg, x) and x not in watched]
# watch the show and add it to watched
for f in sorted(matches):
    print(f)
    if not sp.call(['mpv', wdir+f]):
        watched.append(f)
        print(f)
        save()
