#!/bin/env python3
import sys
import subprocess as sp

# pdb.set_trace()
#video = sp.check_output(['youtube-dl','-g',url])
#v = video.decode('utf-8').split('\n')
url = sp.check_output(['xclip', '-o'])
mpv = sp.call(['mpv', url])
