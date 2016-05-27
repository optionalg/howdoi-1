# Package install/setup

## Setup the 'core' packages for wm/wireless/utilities/etc.
```
# Make sure keys and cache are all clean/setup
sudo pacman -Sc
sudo pacman-key --refresh-keys

sudo pacman -S alsa-utils chromium feh i3 i3lock i3status dmenu gsfonts lxterminal p7zip pandoc screen unzip wpa_supplicant xautolock xorg-xdm network-manager-applet cbatticon volumeicon sshfs

# fonts
sudo pacman -S ttf-liberation ttf-freefont ttf-arphic-uming ttf-baekmuk noto-fonts noto-fonts-cjk noto-fonts-emoji
```

## Setup 'X' and display manager
```
sudo pacman -S xorg-xrandr xorg
sudo systemctl enable xdm.service
```

## Setup iptables
```
sudo ln -s $HOME/.bin/sys/iptables.rules /etc/iptables/iptables.rules
sudo systemctl enable iptables
```

```
cd ~
mkdir -p $HOME/.cache/helper_cache
helper_cache rebuild
```

Reboot

