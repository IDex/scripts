import os
import sys
import re
import json
import subprocess as sp
import argparse

FOLDER = os.path.expanduser('~/new/')

def save():
    with open(os.path.dirname(os.path.realpath(__file__)) +
              '/watched.json', 'w') as f:
        json.dump(watched, f)

def find(searchwords):
    arg = '.*'.join(searchwords)
    watched = []
    try:
        with open(os.path.dirname(os.path.realpath(__file__)) +
                '/watched.json', 'r') as f:
            watched = json.load(f)
    except Exception:
        watched = []
    matches = [x for x in os.listdir(FOLDER)
            if re.search(arg, x, re.IGNORECASE) and x not in watched]
    return matches

def playone(f):
    try:
        print('Playing {}'.format(f))
        return sp.call(['mpv', '--fs', FOLDER+f], stdout=sp.DEVNULL)
    except KeyboardInterrupt:
        SystemExit

def playall(matches):
    try:
        for f in sorted(matches):
            print('Playing {}'.format(f))
            if not sp.call(['mpv', '--fs', FOLDER+f], stdout=sp.DEVNULL):
                watched.append(f)
                print(f)
                save()
    except KeyboardInterrupt:
        SystemExit

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Watch unseen videos in a folder automatically')
    parser.add_argument('-d','--directory', default=FOLDER)
    parser.add_argument('-a','--ask', action='count', default=0)
    parser.add_argument('filename', nargs='*')
    args = parser.parse_args()
    FOLDER = args.directory
    if args.ask:
        for match in find(args.filename):
            ret = playone(match)
            if ret or 'n' in input('Save and play next?[Y/n]\n'):
                break
            else:
                watched.append(match)
                save()
    else:
        playall(find(args.filename))
