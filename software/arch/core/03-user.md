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

setup user
```
su enck
cd ~
mkdir .ssh
chmod 700 .ssh
cd .ssh
<copy authorized keys>
chmod 600 authorized_keys
cd ~
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
```

Define the 'regen' of key
```
vim /home/public/regenerate.sh
---
SSH_HOME="$HOME/.ssh/"
PATH_TO="${SSH_HOME}id_rsa"
OUTPUT_TEXT="/tmp/reg-key"

function print-line()
{
    echo "$1" >> $OUTPUT_TEXT
}

if [ -z "$1" ]; then
    echo "email address required"
    exit -1
fi

echo "when prompted save to $PATH_TO"
echo "save the password!!!"
ssh-keygen -t rsa -b 4096 -C "public@localhost"
mv ${PATH_TO}.pub ${SSH_HOME}authorized_keys
echo -n "Password: "
read -s password
echo
if [ -z "$password" ]; then
    echo "password should not be empty..."
    exit -1
fi
TODAY=$(date +%Y-%m-%d)
print-line "SSH key regenerated ($TODAY)"
print-line "public@localhost"
print-line "password: $password"
mutt -s "SSH public key regen'd ($TODAY)" $1 < $OUTPUT_TEXT -a $PATH_TO
rm $OUTPUT_TEXT
```

Setup for the user
```
chown public:public /home/public/regenerate.sh
chmod u+x /home/public/regenerate.sh
```

Setup the user's ssh profile
```
su public
cd ~
mkdir .ssh
chmod 700 .ssh
./regenerate.sh <address>
```

