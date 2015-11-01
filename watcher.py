#!/bin/env python3
import os
import sys
import re
import json
import subprocess as sp
import argparse

FOLDER = os.path.expanduser('~/new/')


class Watcher:

    def __init__(self, files, folder):
        self.folder = folder
        self.watched = self.load()
        self.matches = self.find(files)

    def save(self):
        with open(os.path.dirname(os.path.realpath(__file__)) +
                  '/watched.json', 'w') as f:
            json.dump(self.watched, f)

    def load(self):
        watched = []
        try:
            with open(os.path.dirname(os.path.realpath(__file__)) +
                      '/watched.json', 'r') as f:
                watched = json.load(f)
        except Exception as e:
            print('{} while loading json'.format(e))
        return watched

    def find(self, files):
        arg = '.*'.join(files)
        matches = [x for x in os.listdir(FOLDER)
                   if re.search(arg, x, re.IGNORECASE) and x not in self.watched]
        return matches

    def playone(self, f=None):
        if not f:
            f = sorted(self.matches).pop()
        print('Playing {}'.format(f))
        if sp.call(['mpv', '--fs', self.folder + f], stdout=sp.DEVNULL):
            return
        else:
            self.watched.append(f)
            self.save()

    def playall(self, nonstop=True):
        for f in sorted(self.matches):
            print('Playing {}'.format(f))
            if nonstop:
                if not sp.call(['mpv', '--fs', self.folder + f], stdout=sp.DEVNULL):
                    self.watched.append(f)
                    self.save()
                else:
                    return
            else:
                if self._ask():
                    return

    def _ask(self):
        if 'n' in input('Play next?[Y/n]'):
            return True
        else:
            return False



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Watch unseen videos in a folder automatically')
    parser.add_argument('-d', '--directory', default=FOLDER, help='Specify directory for videos')
    parser.add_argument('-a', '--ask', action='count', default=0,
                        help='Watch one file at a time and get asked to continue')
    parser.add_argument('searchwords', nargs='*')
    args = parser.parse_args()
    watcher = Watcher(args.searchwords, args.directory)
    if args.ask:
        watcher.playall(ask)
    else:
        watcher.playall()
