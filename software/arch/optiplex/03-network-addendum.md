Network (addendum)
===

Drop dhcp
```
systemctl disable dhcpcd@<interface>.service
```

```
vim /etc/systemd/network/wired.network
---
[Match]
Name=<interface>

[Network]
DHCP=ipv4
```

```
systemctl enable systemd-networkd
systemctl enable systemd-resolved
reboot
```

```
rm -f /etc/resolv.conf
ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf
```
