# User Utility/Helpers

## Necessary packages
```
sudo pacman -S keepassx2 bash-completion rpmextract gconf arch-install-scripts wget ntp tree hexchat vlc
```

## Bash auto-complete
```
sudo ln -s /home/enck/.bin/autocomplete/* /usr/share/bash-completion/completions/
```

## Workspace/container setup
```
sudo su
cd /var/lib/machines
mkdir new
sudo pacstrap -i -c -d new/ base
mkdir /opt/shared
chown enck:enck /opt/shared
mkdir -p /etc/systemd/nspawn
vim /etc/systemd/nspawn/new.nspawn
---
[Files]
Bind=/opt/shared
Bind=/var/cache/pacman
```


## Chrome (google-chrome)
```
sudo mkdir -p /opt/google
sudo mkdir -p /opt/google/chrome
chown -R enck:enck /opt/google/
setup-chrome
```

## NTP

```
sudo systemctl enable ntpd.service
sudo systemctl start ntpd.service
```

## XDM login

To change the xdm login text
```
sudo vim /etc/X11/xdm/Xresources
```

## CAC reader
```
sudo pacman -S ccid opensc
```

```
sudo vim /etc/opensc.conf
---
# comment in enable_pinpad = false (2 places)
```

```
sudo systemctl enable pcscd.service
sudo systemctl start pcscd.service
```

Follow instructions from [here](https://wiki.archlinux.org/index.php/Common_Access_Card)

## Icons

```
pacman -S python python-pip python-gobject
```

## suspend/resume

IF system doesn't work (e.g. systemd upgrade 229 -> 230)
```
sudo vim /etc/systemd/login.conf
---
# set the following
HandleLidSwitchDocked=ignore
LidSwitchIgnoreInhibited=yes
```

## machinectl

Follow [this](https://github.com/enckse/howdoi/blob/master/software/containers/init-nspawn.md)
