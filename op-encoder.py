#!/usr/bin/env python3
"""
Simplify encoding openings/endings for openings.moe
"""
import subprocess as sp
import json
import re
import argparse


class Bunch:
    """Makes dictionary accessible with a.b notation"""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


parser = argparse.ArgumentParser()
parser.add_argument('--start_time', '-s', help='In format hh:mm:ss.sss')
parser.add_argument(
    '--end_time',
    '-e',
    default='00:01:30',
    help='Same format as start, duration, e.g. default 00:01:30')
parser.add_argument('--filename', '-f', help='Source file')
parser.add_argument('--outfile', '-o', default='out.webm',
                    help='Output file, default out.webm')
options = parser.parse_args()

cmd = f'ffmpeg -ss {options.start_time} -i "{options.filename}" -to {options.end_time} -pass 1 -threads 4 -c:v libvpx-vp9 -b:v 3200k -maxrate 3700k -speed 4 -g 240 -slices 4 -vf "scale=-1:min(720\,ih)" -tile-columns 6 -frame-parallel 0 -auto-alt-ref 1 -lag-in-frames 25 -c:a libvorbis -af loudnorm=I=-16:LRA=20:TP=-1:dual_mono=true:linear=true:print_format=json -sn -f webm -y /dev/null'
first_pass = sp.run(
    cmd,
    shell=True,
    stdout=sp.PIPE,
    stderr=sp.STDOUT,
    encoding='utf8')
eq_config = re.split('({[^{]*})', first_pass.stdout)[-2]
eq_config = Bunch(**json.loads(eq_config))
cmd = f'ffmpeg -ss {options.start_time} -i "{options.filename}" -to {options.end_time} -pass 2 -threads 4 -c:v libvpx-vp9 -b:v 3200k -maxrate 3700k -speed 1 -g 240 -slices 4 -vf "scale=-1:min(720\,ih)" -tile-columns 6 -frame-parallel 0 -auto-alt-ref 1 -lag-in-frames 25 -c:a libvorbis -af loudnorm=I=-16:LRA=20:TP=-1:dual_mono=true:linear=true:measured_I={eq_config.input_i}:measured_LRA={eq_config.input_lra}:measured_TP={eq_config.input_tp}:measured_thresh={eq_config.input_thresh}:offset={eq_config.target_offset} -sn -y {options.outfile}'
second_pass = sp.run(cmd, shell=True)
