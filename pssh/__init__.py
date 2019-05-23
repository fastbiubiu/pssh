# !/usr/bin/env python

__author__ = 'dunkebiao'

"Auto ssh login # ssh.py [number] [find(str)]"

import os
import sys
import pexpect


class Pssh:
    help_str = '''usage: pssh [options] [args]
    ssh comand-line client, version 0.2.0.
    This is a line nonsense
Valid options:
    -h [--help]     : Show help
    --list          : Show host list
'''
    conf = [
        # ['user','host','port','passwd']
    ]
    conf_file = os.environ['HOME'] + '/.pssh.conf'
    process = None

    def __init__(self):
        if os.path.exists(self.conf_file):
            try:
                f = open(self.conf_file, 'r')
                for line in f:
                    self.conf.append(line.split())
                f.close()
            except IOError as e:
                sys.exit(e)

    def list(self):
        """
            Display list and input id
        :return: list
        """
        self.show_list()
        try:
            number = input('please input (id):')
        except KeyboardInterrupt as e:
            sys.exit()
        try:
            return self.conf[int(number)]
        except ValueError:
            sys.exit()
        except IndexError:
            sys.exit('[Error] There is no host')

    def show_list(self):
        """
            Display list
        :return: list
        """
        for key, h in enumerate(self.conf):
            print(str(key) + ') ' + h[0])

    def set_win_size(self):
        """
         set windows size
        :return:
        """
        if not self.process:
            return
        terminal = os.get_terminal_size()
        self.process.setwinsize(terminal.lines, terminal.columns)

    def login(self, host):
        """
            Perform login
        :param host:
        """
        self.process = process = pexpect.spawn('ssh %s -p %s -l %s ' % (host[0], host[1], host[2]))

        while True:
            index = process.expect(['continue', 'password:', pexpect.EOF, pexpect.TIMEOUT], timeout=10)
            if index == 0:
                process.sendline('yes')
                continue
            elif index == 1:
                process.sendline(host[3])
                break
            else:
                continue
        self.set_win_size()
        process.interact()
