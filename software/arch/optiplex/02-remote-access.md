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
systemctl enable systemd-resolved
systemctl start systemd-networkd
systemctl start systemd-resolved
rm -f /etc/resolv.conf
ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf
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

