systemd-resolved
===

```
machinectl shell <machine>
systemctl enable systemd-resolved
poweroff
```

```
machinectl shell <machine>
rm -f /etc/resolv.conf
ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf
```
