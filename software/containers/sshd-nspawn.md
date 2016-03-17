systemd-nspawn sshd/ports
---
Simple/basic sshd for localhost (only) with systemd-nspawn

## Install openssh
---
Necessary packages to run ssh
```
pacman -S openssh
```

## Config
---
Config file for sshd
```
vim /etc/ssh/sshd_config
---

ListenAddress 127.0.0.1
Protocol 2
PermitRootLogin yes
RSAAuthentication yes
PubkeyAuthentication yes
AuthorizedKeysFile      .ssh/authorized_keys
PasswordAuthentication no
ChallengeResponseAuthentication no
UsePAM yes
Subsystem       sftp    /usr/lib/ssh/sftp-server
Port <number> # will be generated automatically at profile load 
```

## Loading sshd at profile load
---
Use '--setenv INPUT_SSHD_PORT' to enable binding SSH to that port
```
vim /etc/profile.d/container.sh
---
#!/bin/bash
if [ ! -z "$INPUT_SSHD_PORT" ]; then
    SSHD_FILE=/etc/ssh/sshd_config
    ssh_pid=$(pidof sshd)
    if [ -z "$ssh_pid" ]; then
        ssh_port="$INPUT_SSHD_PORT"
        current_ssh_config=$(cat $SSHD_FILE | grep -v "^Port")
        echo "$current_ssh_config" > $SSHD_FILE
        echo "Port $ssh_port" >> $SSHD_FILE
        /usr/bin/ssh-keygen -A
        pkill sshd
        /sbin/sshd
    fi

    using_port=$(cat $SSHD_FILE | grep "^Port" | sed 's/Port //g')
    echo "ssh root@localhost -p $using_port"
fi
```

Make sure it is executable
```
chmod u+x /etc/profile.d/container
```

## Configuring user/ssh settings
---
Setup a user for ssh
```
cd ~
mkdir .ssh
chmod 700 .ssh
cp <pubkey> .ssh/authorized_keys
chmod 600 .ssh/authorized_keys
chown -R $USER:$USER .ssh/
```

Make a quick reference guide as well
```
ln -s /etc/profile.d/container.sh /usr/local/bin/container-info
```
