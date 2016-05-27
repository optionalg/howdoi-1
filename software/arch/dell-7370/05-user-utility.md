# User Utility/Helpers

## Necessary packages
```
sudo pacman -S keepassx2 bash-completion rpmextract gconf arch-install-scripts wget ntp tree
```

## Bash auto-complete
```
sudo ln -s /home/enck/.bin/autocomplete/* /usr/share/bash-completion/completions/
```

## Workspace/container setup
```
sudo mkdir /opt/workspace
chown enck:enck /opt/workspace
sudo mkdir /opt/workspace/containers
cd /opt/workspace/containers
sudo mkdir template
sudo pacstrap -i -c -d template/ base
cd ~
mkdir /opt/workspace/container-bin
mkdir /opt/workspace/shared
ln -s /opt/workspace/shared/ workspace
```


## Chrome (google-chrome)
```
sudo mkdir -p /opt/google
sudo mkdir -p /opt/google/chrome
helper_cache setup-chrome
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

Follow instructions from [here](https://github.com/enckse/howdoi/blob/master/software/chrome/dod-certs.md)

