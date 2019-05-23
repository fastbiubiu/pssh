# !/usr/bin/env python

import pssh
import getopt
import signal
import sys

"""
    This is main. you: nonsense.
"""
try:
    options, args = getopt.getopt(
        sys.argv[1:],
        'hs:i:c:',
        ['list', 'help']
    )
except getopt.GetoptError as e:
    sys.exit(e.msg)

pssh = pssh.Pssh()


def set_win_size(signum, frame):
    pssh.set_win_size()


signal.signal(signal.SIGWINCH, set_win_size)

operator = pssh.login
host = []

for name, value in options:
    if name == '--list':
        pssh.show_list()
        exit()
    if name in ('-h', '--help'):
        print(pssh.help_str)
        exit()

if not host:
    host = pssh.list()

operator(host)
