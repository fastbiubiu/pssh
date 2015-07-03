#!/usr/bin/env python
# coding=utf-8

__author__ = 'dunkebiao'

"auto ssh login # ssh.py [number] [find(str)]"

import os
import sys
import getopt
import hashlib


class Pssh:
    h_list = [
        # ['user','host','port','passwd']
    ]
    options = ''
    h_conf = os.environ['HOME'] + '/.pssh.conf'
    f_exp = ''
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

    def __init__(self):

        if not self.h_list and os.path.exists(self.h_conf):
            try:
                f = open(self.h_conf, 'r')
                for line in f:
                    self.h_list.append(line.split())
                f.close()
            except IOError, e:
                sys.exit(e)

            try:
                self.options, args = getopt.getopt(sys.argv[1:], 's:d:', ['scp'])
            except getopt.GetoptError, e:
                sys.exit(e.msg)

    def find(self, h_id):
        return self.h_list[h_id]

    def search(self, h_str):
        self.h_list = [x for x in self.h_list if x[1].find(h_str) != -1]

        if len(self.h_list) == 0:
            sys.exit('[Error] There is no host')
        elif len(self.h_list) == 1:
            return self.h_list[0]
        elif len(self.h_list) > 1:
            for key, h in enumerate(self.h_list):
                print str(key) + ') ' + h[1]

            number = raw_input('please input (id):\r\n')
            if not number.isdigit() or not self.h_list[int(number)]:
                sys.exit('[Error] There is no host')

            return self.h_list[int(number)]

    def add(self, host, user, passwd, port):
        pass

    def expect(self, cmd):
        self.f_exp = '/tmp/' + hashlib.md5(cmd)
        if not os.path.exists(self.f_exp):
            try:
                f = open(self.f_exp, 'a+')
                f.writelines(cmd)
                f.close()
            except IOError, e:
                sys.exit(e)
            os.system('chmod +x ' + self.f_exp)

    def login(self):
        self.expect(self.login_cmd)
        os.system(self.f_exp + ' %s %s %s %s' % tuple(h_list[int(number)]))

    def scp(self):
        self.expect(self.scp_cmd)
        os.system(self.f_exp + ' %s %s %s %s' % tuple(h_list[int(number)]))

    def __del__(self):
        os.remove(self.f_exp)


def main():
    pass


if __name__ == '__main__':
    main()
