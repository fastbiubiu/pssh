# pssh
ssh manage

### host config file. default ~/.pssh.conf
    pssh -c [~/.pssh.conf]

### show host list
    pssh --list

### add host
    pssh --add [host] [port] [user] [passwd]

### del host
    pssh --del -d [number]
    pssh --del -s [str]

### pull
    pssh --pull [local] [remote]
    pssh --pull -d [number] [remote] [local]
    pssh --pull -s [str] [remote] [local]
    pssh --pull -c [~/.pssh.conf] -s [str] [remote] [local]

### push
    pssh --push [local] [remote]

### search by id list
    pssh -d [number]

### keyword search through the list
    pssh -s [str]