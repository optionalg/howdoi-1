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

Follow [this](https://github.com/enckse/howdoi/blob/master/software/containers/init-nspawn.md)
