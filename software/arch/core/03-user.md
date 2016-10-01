# Root login/post install reboot

## Cleaning up from install
```
pacman -Sc
pacman-key --refresh-keys
```

## Start installing user settings/configuring user access
```
vim /etc/ssh/sshd_config
---
Port <PORT>
Protocol 2
PermitRootLogin no
PasswordAuthentication no
```

and start
```
systemctl enable sshd
systemctl start sshd
```

```
su enck
ln -s /mnt/Storage/ store
ln -s /mnt/Storage/Git git
exit
```

## NTP
```
pacman -S ntp
systemctl enable ntpd
systemctl start ntpd
```

## Config git
```
# as root and enck
git config --global push.default simple
git config --global core.editor "vim"
git config --global user.name "<name>"
git config --global user.email "<email>"
git config --global core.autocrlf input
```

## Core scripts
```
pacman -S smartmontools cronie ssmtp wget mutt
```

```
cd /opt/core
cat cron | crontab -
systemctl enable cronie
```

Copy or define ssmtp setup and test
```
echo test | mail -v -s "testing" <email>
```

## Gateway/rotating user
Setup the user
```
useradd -m -s /bin/bash public
passwd public
su public
cd ~
mkdir .ssh
chmod 700 .ssh
```
