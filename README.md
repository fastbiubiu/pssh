# pssh
ssh manage

### config file:
    ~/.pssh.conf

### show host list
    pssh --list

### add host
    pssh --add [host] [port] [user] [passwd]

### del host
    pssh --del -d [number]
    pssh --del -s [str]

### scp
    pssh --scp -d [number] [source] [destination]


### search by id list
    pssh -d [number]

### keyword search through the list
    pssh -s [str]

