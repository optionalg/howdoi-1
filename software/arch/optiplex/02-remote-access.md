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
pacman -S openssh wget bash-completion ntp
systemctl enable ntpd
systemctl start ntpd
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

* setup [rank-mirrors](https://github.com/epiphyte/rank-mirrors)
* setup [client](https://github.com/enckse/clients)

```
exit
```

## Setup iptables
```
# make sure to change <PORT>
vim /etc/iptables/iptables.rules
---
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
:TCP - [0:0]
:UDP - [0:0]
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -m conntrack --ctstate INVALID -j DROP
-A INPUT -p icmp -m icmp --icmp-type 8 -m conntrack --ctstate NEW -j ACCEPT
-A INPUT -p udp -m conntrack --ctstate NEW -j UDP
-A INPUT -p tcp --tcp-flags FIN,SYN,RST,ACK SYN -m conntrack --ctstate NEW -j TCP
-A INPUT -p udp -j REJECT --reject-with icmp-port-unreachable
-A INPUT -p tcp -j REJECT --reject-with tcp-reset
-A INPUT -j REJECT --reject-with icmp-proto-unreachable

-A TCP -p tcp --dport <PORT> -j ACCEPT

COMMIT
```

## Enabling firewall
```
systemctl enable iptables
systemctl start iptables
```
