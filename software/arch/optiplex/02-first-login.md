# Root login/post install reboot

## Setup a user
```
useradd -m -s /bin/bash enck
passwd enck
```

## Make sure networking/dhcp (wired) is available
```
systemctl enable dhcpcd@<adapter>.service
systemctl start dhcpcd@<adapter>.service
```

## Setup user sudo'ing for wheel, add user to wheel
```
pacman -S sudo
usermod -G wheel enck
visudo
#uncomment %wheel ALL=(ALL) ALL
```

## Networking/system utilities
```
pacman -S openssh wget bash-completion arch-install-scripts screen
```

# User configuration/bootstrapping


## Move into that user
```
su enck
cd ~
rm .bash*
```

## Configure git
```
git config --global core.excludesfiles ~/.config/.gitignore
git config --global push.default simple
git config --global core.editor "vim"
git config --global user.name "<name>"
git config --global user.email "<email>"
git config --global core.autocrlf input
```

## Bash profile
```
wget https://raw.githubusercontent.com/enckse/home/master/.bash_profile
wget https://raw.githubusercontent.com/enckse/home/master/.bashrc
cat .bashrc | head -n 60 > .bashrc.tmp
mv .bashrc.tmp .bashrc
wget https://raw.githubusercontent.com/enckse/home/master/.vimrc
```

## Cleanup in pacman
```
exit # user context
pacman -Sc
pacman-key --refresh-keys
```

## Setup iptables
```
# make sure to change <PORT>
vim /etc/iptables/iptables.rules
---
*filter
:INPUT DROP [11:1508]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [219:35101]
-A INPUT -i lo -j ACCEPT
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p tcp -m tcp --dport <PORT> -j ACCEPT
-A OUTPUT -p tcp -m tcp --sport <PORT> -m state --state RELATED,ESTABLISHED -j ACCEPT
COMMIT
```

## Enabling firewall
```
systemctl enable iptables
systemctl start iptables
reboot
```

## Workspace/container setup
```
# as root
mkdir /opt/workspace
mkdir /opt/workspace/containers
cd /opt/workspace/containers
mkdir template
pacstrap -i -c -d template/ base
chown enck:enck -R /opt/workspace
```

## Configure nspawn

Follow [this](https://github.com/enckse/howdoi/blob/master/software/containers/init-nspawn.md)
```
curl https://raw.githubusercontent.com/enckse/home/master/.bin/machinectl-helper > /usr/local/bin/machinectl-helper
chmod u+x /usr/local/bin/machinectl-helper
```

## SSH(d)
```
# configure the following
vim /etc/ssh/sshd_config
---
Port <PORT>
Protocol 2
# may need to enable, for a moment, to copy keys
PermitRootLogin no
PasswordAuthentication no
```

```
systemctl enable sshd
systemctl start sshd
```

## speaker

```
vim /etc/modprobe.d/nobeep.conf
---
blacklist pcspkr
```

