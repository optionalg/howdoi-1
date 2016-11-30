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
pacstrap -i -c -d new/ base
chown enck:enck /opt/shared
mkdir -p /etc/systemd/nspawn

```
vim /etc/systemd/nspawn/new.nspawn
---
[Files]
Bind=/opt/shared
Bind=/var/cache/pacman
BindReadOnly=/etc/vimrc
BindReadOnly=/etc/pacman.d/mirrorlist.ranked
BindReadOnly=/etc/pacman.conf
BindReadOnly=/home/enck.gitconfig:/root/.gitconfig
BindReadOnly=/home/enck/.config/.gitignore
```

```
vim /etc/pacman.conf
---
# for each repo, add Include=/etc/pacman.d/mirrorlist.ranked
```


## Chrome (google-chrome)
```
mkdir -p /opt/google
mkdir -p /opt/google/chrome
chown -R enck:enck /opt/google/
exit
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

## machinectl

Follow [this](../../containers/init-nspawn.md)

## ALSA

Get the 'right' sound card defaulted in
```
vim /etc/asound.conf
---
pcm.!default {
	type plug
	slave {
		pcm "hw:1,0"
	}
}

ctl.!default {
	type hw
	card 1
}
```

## Disable bluetooth
```
sudo pacman -S rfkill
sudo systemctl enable rfkill-block@bluetooth.service
sudo systemctl start rfkill-block@bluetooth.service
```

## Blacklist speaker

Blacklist the pc-speaker...
```
echo "blacklist pcspkr" > /etc/modprobe.d/nobeep.conf
```
