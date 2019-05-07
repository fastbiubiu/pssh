# pssh
ssh manages

### Install
    curl -sS https://raw.githubusercontent.com/dunkebiao/pssh/master/install | python - --filename=pssh --install-dir=/usr/local/bin

### Host config file, default ~/.pssh.conf
    pssh -c [~/.pssh.conf]

### Add host
    pssh --add [host] [port] [user] [passwd]

### Del host
    pssh --del -d [number]

### Show host list
    pssh --list
    
### Search by id list
    pssh -d [number]

### Keyword search through the list
    pssh -s [str]
    
### Pull, warning: remote  ~/ rewrite '~/'
    pssh --pull [remote] [local]

### Push
    pssh --push [local] [remote]
