Added items
---

## suspend/resume

IF system doesn't work (e.g. systemd upgrade 229 -> 230)
```
sudo vim /etc/systemd/login.conf
---
# set the following
HandleLidSwitchDocked=ignore
LidSwitchIgnoreInhibited=yes
```

## Cache

```
cd .cache
ln -s /mnt/Synced/cache/misc/* .
ln -s /mnt/Synced/cache/nspawn .
ln -s /mnt/Synced/cache/urls/* dmenu_urls/
```

## machinectl

```
systemctl enable machines.target
```

```
sudo systemctl edit systemd-nspawn@.service
---
[Service]
ExecStart=
ExecStart=/usr/bin/systemd-nspawn --quiet --keep-unit --boot --link-journal=try-guest --machine=%I
```
