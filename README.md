# pssh
ssh manage

### Install
    curl -sS https://raw.githubusercontent.com/dunkebiao/pssh/master/install | python - --filename=pssh —install-dir=/usr/local/bin

### Host config file, default ~/.pssh.conf, warning: please put in start
    pssh -c [~/.pssh.conf]

### Show host list
    pssh --list

### Add host
    pssh --add [host] [port] [user] [passwd]

### Del host
    pssh --del -d [number]
    pssh --del -s [str]

### Pull, warning: remote  ~/ rewrite '~/'
    pssh --pull [local] [remote]
    pssh --pull -d [number] [remote] [local]
    pssh --pull -s [str] [remote] [local]
    pssh --pull -c [~/.pssh.conf] -s [str] [remote] [local]

### Push
    pssh --push [local] [remote]

### Search by id list
    pssh -d [number]

### Keyword search through the list
    pssh -s [str]