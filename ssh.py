#!/usr/bin/env python
# coding=utf-8

__author__ = 'dunkebiao'

"Auto ssh login # ssh.py [number] [find(str)]"

import os
import sys
import getopt
import hashlib


class Pssh:
    login_cmd = '''#!/usr/bin/expect
set user [lindex $argv 0]
set host [lindex $argv 1]
set port [lindex $argv 2]
set passwd [lindex $argv 3]
spawn ssh $host -p $port -l $user
expect {
    "yes/no" {send "yes\r";exp_continue}
    "password:" {send "$passwd\r"}
}
interact
'''
    scp_cmd = '''#!/usr/bin/expect
set user [lindex $argv 0]
set host [lindex $argv 1]
set port [lindex $argv 2]
set passwd [lindex $argv 3]
spawn ssh $host -p $port -l $user
expect {
    "yes/no" {send "yes\r";exp_continue}
    "password:" {send "$passwd\r"}
}
interact
'''
    help_str = '''usage: pssh [options] [args]
    ssh comand-line client, version 0.1.0.
    This is a line nonsense
Valid options:
    -h [--help]     : Show help
    -d [--id]       : By id lookup
    -s [--search]   : Through the keyword search
    --scp           : The remote copy files
'''
    h_list = [
        # ['user','host','port','passwd']
    ]
    options = ''
    h_conf = os.environ['HOME'] + '/.pssh.conf'
    f_exp = ''

    def __init__(self):

        if os.path.exists(self.h_conf):
            try:
                f = open(self.h_conf, 'r')
                for line in f:
                    self.h_list.append(line.split())
                f.close()
            except IOError, e:
                sys.exit(e)

        if len(self.h_list) == 0:
            sys.exit('[Error] There is no host')

    def find(self, h_id):
        """
            Search by id list
        :param h_id: int
        :return: list
        """
        try:
            return self.h_list[int(h_id)]
        except IndexError:
            sys.exit('[Error] There is no host')

    def search(self, h_str):
        """
            Keyword search through the list
        :param h_str: str
        :return: list
        """
        self.h_list = [x for x in self.h_list if x[1].find(h_str) != -1]

        if len(self.h_list) == 1:
            return self.h_list[0]
        elif len(self.h_list) > 1:
            return self.list
        else:
            sys.exit('[Error] There is no host')

    @property
    def list(self):
        """
            Display list and input id
        :return: list
        """
        for key, h in enumerate(self.h_list):
            print str(key) + ') ' + h[1]

        number = raw_input('please input (id):\r\n')
        try:
            return self.h_list[int(number)]
        except IndexError:
            sys.exit('[Error] There is no host')

    def add(self, host, user, passwd, port):
        """
            Add the host
        :param host:
        :param user:
        :param passwd:
        :param port:
        """
        pass

    def expect(self, cmd):
        """
            To expect command file
        :param cmd: str
        """
        m = hashlib.md5()
        m.update(cmd)
        self.f_exp = '/tmp/' + m.hexdigest()

        if not os.path.exists(self.f_exp):
            try:
                f = open(self.f_exp, 'a+')
                f.writelines(cmd)
                f.close()
            except IOError, e:
                sys.exit(e)
            os.system('chmod +x ' + self.f_exp)

    def login(self, host):
        """
            Perform login
        :param host:
        """
        self.expect(self.login_cmd)
        try:
            os.system(self.f_exp + ' %s %s %s %s' % tuple(host))
        except:
            sys.exit('[Error] Logon failure')

    def scp(self, host):
        """
            Perform scp
        :param host:
        """
        self.expect(self.scp_cmd)
        try:
            os.system(self.f_exp + ' %s %s %s %s' % tuple(host))
        except:
            sys.exit('[Error] scp failure')

    def __del__(self):
        # os.remove(self.f_exp)
        pass


def main():
    """
        This is main. you: nonsense.
    """
    try:
        options, args = getopt.getopt(sys.argv[1:], 'hs:d:', ['scp', 'id=', 'search=', 'help'])
    except getopt.GetoptError, e:
        sys.exit(e.msg)

    pssh = Pssh()
    operator = pssh.login
    host = []

    for name, value in options:
        if name in ('-d', 'id'):
            host = pssh.find(int(value))
        if name in ("-s", "--search"):
            host = pssh.search(str(value))
        if name in ('--scp'):
            operator = pssh.scp
        if name in ('-h', '--help'):
            exit(pssh.help_str)

    if not host:
        host = pssh.list

    operator(host)


if __name__ == '__main__':
    main()
