# Root login/post install reboot

## Make sure networking/dhcp (wired) is available
```
vim /etc/systemd/network/wired.network
---
[Match]
Name=<adapter>

[Network]
DHCP=ipv4
```

```
systemctl enable systemd-networkd
systemctl start systemd-networkd
vim /etc/resolv.conf
---
nameserver <local nameserver>
nameserver <public nameservers...>
```

## Setup a user
```
# foreach user
useradd -m -s /bin/bash <user>
passwd <user>
```

## Setup user sudo'ing for wheel, add user to wheel
```
pacman -S sudo
usermod -G wheel <user>
visudo
#uncomment %wheel ALL=(ALL) ALL
```

## Networking/system utilities
```
pacman -S openssh wget bash-completion
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

```
su enck
mkdir .ssh
chmod 700 .ssh
# copy pubkey
chmod 600 .ssh/authorized_keys
```

setup [client](https://github.com/enckse/clients)

```
exit
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
```
