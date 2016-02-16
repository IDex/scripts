#!/bin/env python3
"""
Watch unseen videos in a folder automatically
"""
import os
import re
import json
import subprocess as sp
import argparse

FOLDER = os.path.expanduser('~/anim/')
PROG = 'mpv --fs --alang=jpn,en --slang=jpn,en'
FILETYPES = ['mkv']


class Watcher:
    """
    Shows unwatched videos in a folder.
    """

    def __init__(self, files, folder, nosave=False, player=None, filetypes=None, deep_search=False):
        self.savefile = '/watched.json'
        self.folder = folder
        self.nosave = nosave
        self.player = player
        self.deep_search = deep_search
        self.filetypes = filetypes
        self.watched = self.load()
        self.matches = self.find(files)

    def save(self):
        """Save watched files, unless forbidden"""
        if not self.nosave:
            with open(os.path.dirname(os.path.realpath(__file__)) +
                      self.savefile, 'w') as f:
                json.dump(self.watched, f)

    def load(self):
        """Load watched videos in the directory and return them."""
        watched = []
        try:
            with open(os.path.dirname(os.path.realpath(__file__)) +
                      self.savefile, 'r') as f:
                watched = json.load(f)
        except Exception as e:
            print('{} while loading json'.format(e))
        return watched

    def find(self, search_words, include_watched=False, deep_search=False):
        """Find files from video dir that match search words."""
        search_words.extend(self.filetypes)
        arg = '.*'.join(search_words)
        if deep_search or self.deep_search:
            files = [f for b in os.walk(self.folder) for f in b[2]]
        else:
            files = os.walk(self.folder).__next__()[2]
        if include_watched:
            matches = list({x for x in self.watched + files
                            if re.search(arg, x, re.IGNORECASE)})
        else:
            matches = [x for x in files
                       if re.search(arg, x, re.IGNORECASE) and
                       x not in self.watched]
        return matches

    def clear(self, regex):
        """
        Clear files specified by regex from watched or the last one watched.
        """
        if regex:
            to_be_removed = self.find(regex, include_watched=True)
            self.watched = [x for x in self.watched if x not in to_be_removed]
        else:
            self.watched.pop()
        self.save()

    def remove(self):
        """Remove watched from watched directory"""
        for f in self.watched:
            try:
                os.remove(self.folder + f)
            except (FileNotFoundError, IsADirectoryError):
                print('Missing file:', f)
            else:
                print('Removed file:', self.folder + f)

    def playone(self, f=None):
        """Play one file from unwatched"""
        if not f:
            f = sorted(self.matches).pop()
        print('Playing {}'.format(f))
        if sp.call(['mpv', '--fs', self.folder + f], stdout=sp.DEVNULL):
            return
        else:
            self.watched.append(f)
            self.save()

    def playall(self, nonstop=False):
        """Play all files that match"""
        for f in sorted(self.matches):
            print('Playing {}'.format(f))
            if not sp.call([*self.player.split(), self.folder + f],
                           stdout=sp.DEVNULL):
                self.watched.append(f)
                self.save()
            elif nonstop:
                continue
            else:
                return

    @staticmethod
    def _ask():
        if 'n' in input('Play next?[Y/n]'):
            return True
        else:
            return False


def main():
    """
    Handle argument interpretation
    """
    parser = argparse.ArgumentParser(
        description=__doc__)
    parser.add_argument('-d', '--directory', default=FOLDER, nargs='?', const='./',
                        help='Specify directory for videos')
    parser.add_argument('-p', '--player', default=PROG, nargs='?',
                        help='Specify alternative player command for videos')
    parser.add_argument('-ns', '--nonstop', action='store_true', default=False,
                        help='Watch one file at a time, get asked to continue')
    parser.add_argument('-c', '--clear', action='count',
                        help='Clear last seen/regex from watched.json')
    parser.add_argument('-n', '--nosave', action='store_true', default=False,
                        help="Don't save watched videos")
    parser.add_argument('-r', '--remove', action='store_true', default=False,
                        help='Remove watched files from watched directory')
    parser.add_argument('-i', '--ignore', action='store_true', default=False,
                        help='Watch everything in folder, ignore history')
    parser.add_argument('-l', '--list', action='store_true', default=False,
                        help='List watchable files instead of watching them')
    parser.add_argument('-ds', '--deepsearch', action='store_true', default=False,
                        help='Also play all the files in the subdirectories of main directory')
    parser.add_argument('-lw', '--listwatched', action='store_true',
                        default=False, help='List watched files')
    parser.add_argument('searchwords', nargs='*')
    args = parser.parse_args()
    watcher = Watcher(args.searchwords,
                      args.directory,
                      nosave=args.nosave,
                      player=args.player,
                      filetypes=FILETYPES,
                      deep_search=args.deepsearch)
    if args.remove:
        watcher.remove()
        raise SystemExit
    if args.clear:
        watcher.clear(args.searchwords)
        raise SystemExit
    if args.ignore:
        watcher.matches = watcher.find(args.searchwords, include_watched=True)
        watcher.nosave = True
    if args.list:
        for f in sorted(watcher.matches):
            print(f)
        raise SystemExit
    if args.listwatched:
        for f in watcher.watched:
            print(f)
        raise SystemExit
    if args.nonstop:
        watcher.playall(nonstop=True)
    else:
        watcher.playall()

if __name__ == '__main__':
    main()
