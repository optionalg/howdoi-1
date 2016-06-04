Added items
---

IF system doesn't work (e.g. systemd upgrade 229 -> 230)
```
sudo vim /etc/systemd/login.conf
---
# set the following
HandleLidSwitchDocked=ignore
LidSwitchIgnoreInhibited=yes
```
