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
set host [lindex $argv 0]
set port [lindex $argv 1]
set user [lindex $argv 2]
set passwd [lindex $argv 3]
spawn ssh $host -p $port -l $user
expect {
    "yes/no" {send "yes\r";exp_continue}
    "password:" {send "$passwd\r"}
}
interact
'''
    pull_cmd = '''#!/usr/bin/expect
set host [lindex $argv 0]
set port [lindex $argv 1]
set user [lindex $argv 2]
set passwd [lindex $argv 3]
spawn scp -r -P $port $user@$host:%s %s
expect {
    "yes/no" {send "yes\r";exp_continue}
    "password:" {send "$passwd\r"}
}
interact
'''
    push_cmd = '''#!/usr/bin/expect
set host [lindex $argv 0]
set port [lindex $argv 1]
set user [lindex $argv 2]
set passwd [lindex $argv 3]
spawn scp -r -P $port %s $user@$host:%s
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
    -c              : Load config file, please put in start
    -i [--id]       : By id lookup
    -s [--search]   : Through the keyword search
    --list          : Show host list
    --pull          : Remote copy files to local
    --push          : Local copy files to remote
    --add           : Add host [ip] [prot] [user] [passwd]
    --del           : del host
'''
    h_list = [
        # ['user','host','port','passwd']
    ]
    h_conf = os.environ['HOME'] + '/.pssh.conf'
    f_exp = ''
    cp_file = []

    def __init__(self):
        self.conf()

    def conf(self):
        self.h_list = []
        if os.path.exists(self.h_conf):
            try:
                f = open(self.h_conf, 'r')
                for line in f:
                    self.h_list.append(line.split())
                f.close()
            except IOError, e:
                sys.exit(e)

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

    def list(self):
        """
            Display list and input id
        :return: list
        """
        self.show_list()
        try:
            number = raw_input('please input (id):')
        except IOError, e:
            sys.exit(e)
        try:
            return self.h_list[int(number)]
        except IndexError:
            sys.exit('[Error] There is no host')

    def show_list(self):
        """
            Display list
        :return: list
        """
        for key, h in enumerate(self.h_list):
            print str(key) + ') ' + h[0]

    def add_h(self, host):
        """
            Add the host
        :param host:list
        """
        try:
            f = open(self.h_conf, 'a+')
            f.write('\t'.join([str(x) for x in host]) + '\n')
            f.close()
        except IOError, e:
            sys.exit(e)
        exit('ok\r\n')

    def del_h(self, host):
        """
            Del the host
        :param host:list
        """
        try:
            del self.h_list[self.h_list.index(host)]
        except IndexError, e:
            sys.exit(e)
        try:
            f = open(self.h_conf, 'w')
            for host in self.h_list:
                f.write('\t'.join([str(x) for x in host]) + '\n')
            f.close()
        except IOError, e:
            sys.exit(e)
        exit('ok\r\n')

    def expect(self, cmd):
        """
            To expect command file
        :param cmd: str
        """
        m = hashlib.md5()
        m.update(cmd)
        self.f_exp = '/tmp/' + m.hexdigest()

        try:
            f = open(self.f_exp, 'w')
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

    def push(self, host):
        """
            Perform push file
        :param host:
        """
        self.expect(self.push_cmd % tuple(self.cp_file))
        try:
            os.system(self.f_exp + ' %s %s %s %s' % tuple(host))
        except:
            sys.exit('[Error] push failure')

    def pull(self, host):
        """
            Perform pull file
        :param host:
        """
        self.expect(self.pull_cmd % tuple(self.cp_file))
        try:
            os.system(self.f_exp + ' %s %s %s %s' % tuple(host))
        except:
            sys.exit('[Error] pull failure')

    def __del__(self):
        # os.remove(self.f_exp)
        pass


def main():
    """
        This is main. you: nonsense.
    """
    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            'hs:i:c:',
            ['add', 'del', 'pull', 'push', 'list', 'id=', 'search=', 'help']
        )
    except getopt.GetoptError, e:
        sys.exit(e.msg)

    pssh = Pssh()
    operator = pssh.login
    host = []

    for name, value in options:
        if name in ('-c'):
            pssh.h_conf = value
            pssh.conf()
        if name in ('-i', 'id'):
            host = pssh.find(int(value))
        if name in ("-s", "--search"):
            host = pssh.search(str(value))
        if name in ('--list'):
            pssh.show_list()
            exit(0)
        if name in ('--push'):
            pssh.cp_file = args
            operator = pssh.push
        if name in ('--pull'):
            pssh.cp_file = args
            operator = pssh.pull
        if name in ('--add'):
            host = args
            operator = pssh.add_h
        if name in ('--del'):
            operator = pssh.del_h
        if name in ('-h', '--help'):
            exit(pssh.help_str)

    if not host:
        host = pssh.list()

    operator(host)


if __name__ == '__main__':
    main()
