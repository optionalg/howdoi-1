Gateway/SSH Node
================
* Requires to be 'booted' for ssh to start/act as a service (systemd-nspawn with '-b')
* Setup as root, SSH'ing is done as non-root
* Make sure a 'normal' user is configured (useradd, chown'd $HOME, etc.)

Make sure sshd is installed
```
pacman -S openssh
```

Edit/modify these settings to validate/verify proper config

```
vim /etc/ssh/sshd_config
---
Port <desired>

PermitRootLogin no

AuthorizedKeysFile    %h/.ssh/authorized_keys

PasswordAuthentication no
```

Using a 'regular' user so make sure it is set before entering as them

```
su <user> 
```

Configure ssh private key auth for the user
```
cd ~
mkdir .ssh
chmod 700 .ssh

#<copy key(s) to authorized_keys>
chmod 600 authorized_keys

# leave user context
exit
```

Start/enable the service
```
systemctl enable sshd
systemctl start sshd
```
