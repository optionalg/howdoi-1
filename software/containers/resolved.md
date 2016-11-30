systemd-resolved
===

```
machinectl shell <machine>
systemctl enable systemd-resolved
poweroff
```

```
machinectl start <machine>
machinectl shell <machine>
rm -f /etc/resolv.conf
ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf
```

* https://github.com/systemd/systemd/issues/3649
