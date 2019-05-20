
__author__ = 'dunkebiao'

"Auto ssh login # ssh.py [number] [find(str)]"

import os
import sys
import getopt
import paramiko
from pssh import interactive
import warnings

warnings.filterwarnings("ignore")


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

    def login(self, host):
        """
            Perform login
        :param host:
        """
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(*host)
        chan = client.invoke_shell()
        interactive.interactive_shell(chan)
        chan.close()
        client.close()


def main():
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

    pssh = Pssh()
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

