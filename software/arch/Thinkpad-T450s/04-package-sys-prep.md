# Package install/setup

## Setup the 'core' packages for wm/wireless/utilities/etc.
```
# Make sure keys and cache are all clean/setup
sudo pacman -Sc
sudo pacman-key --refresh-keys

sudo pacman -S alsa-utils chromium feh i3 i3lock i3status dmenu gsfonts lxterminal p7zip pandoc screen unzip wpa_supplicant xautolock xorg-xdm network-manager-applet cbatticon volumeicon
/sbin/reboot
```

## Setup 'X' and display manager
```
sudo pacman -S xorg-xrandr xorg
sudo systemctl enable xdm.service
sudo systemctl start xdm.service
```

## Setup iptables
```
sudo ln -s $HOME/.bin/sys/iptables.rules /etc/iptables/iptables.rules
sudo systemctl enable iptables
sudo systemctl start iptables
```

## Enable touchpad
```
# Install package
sudo pacman -S xf86-input-synaptics libsynaptics
sudo cp /usr/share/X11/xorg.conf.d/50-synaptics.conf /etc/X11/xorg.conf.d/
```

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
