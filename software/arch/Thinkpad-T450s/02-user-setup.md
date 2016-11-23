# User setup

## Setup a user
```
useradd -m -s /bin/bash enck
passwd enck
```

## Make sure networking/dhcp (wired) is available
```
systemctl enable dhcpcd.service
systemctl start dhcpcd.service
```

## Setup user sudo'ing for wheel, add user to wheel
```
pacman -S sudo
visudo
#uncomment %wheel ALL=(ALL) ALL
usermod -G wheel enck
```

## Move into that user
```
mkdir /opt/shared
su enck
cd ~
ln -s /opt/shared workspace
rm .bash*
```

## Setup shares for later
```
sudo mkdir /mnt/Storage
sudo mkdir /mnt/usb
sudo mkdir /mnt/crypt
sudo chown enck:enck /mnt/Storage
sudo chown enck:enck /mnt/crypt
```

## Get initial bootstrapping data
```
# Need scp/ssh and rsync for sync'ing
sudo pacman -S openssh rsync exfat-utils
```

* Need to get the copied data locally (via usb from another machine)

## Bootstrapping crypt
```
mount /dev/<usb> /mnt/usb
mv /mnt/usb/.synced ~
chown -R enck:enck ~/.synced
cp ~/.synced/crypt.img /tmp/crypt.img
sudo cryptsetup luksOpen --readonly /tmp/crypt.img crypt-tmp
sudo mount /dev/mapper/crypt-tmp /mnt/crypt
umount /mnt/usb
```

## Setting up $HOME
```
cd ~
chown enck:enck -R ~/.synced
git init
git remote add origin https://github.com/enckse/home.git
git fetch
rm .bash*
git pull origin master
mkdir .ssh
ln -s ~/.synced/ssh/config ~/.ssh/config
git remote remove origin
git remote add origin git@github.com:enckse/home.git

cd ~
mkdir Downloads
mkdir .tmp
.bin/mounting crypt
# there may be warnings about ssh-agent (not configured yet!)

# Verify host key for sync service (later)
ssh sync
```

## Setup symlinks

```
cd ~
mkdir -p ~/.cache
mkdir -p ~/.config
mkdir -p ~/.config/hexchat
mkdir -p ~/.cache/dmenu_urls
ln -s $HOME/.synced/configs/.gitconfig .gitconfig
ln -s $HOME/.synced/configs/urls/suite.index $HOME/.cache/dmenu_urls/
ln -s $HOME/.synced/configs/urls/urls.index $HOME/.cache/dmenu_urls/
ln -s $HOME/.synced/configs/servlist $HOME/.config/hexchat/
sudo rm /etc/hosts
sudo ln -s ~/.synced/configs/hosts /etc/hosts
sudo rm /etc/vimrc
sudo ln -s ~/.vimrc /etc/vimrc
sudo rm /etc/pacman.d/mirrorlist
mkdir -p ~/.cache/hosted
touch ~/.cache/hosted/mirrorlist
sudo ln -s ~/.cache/hosted/mirrorlist /etc/pacman.d/mirrorlist
.bin/dmenu_urls --rebuild
.bin/dmenu_urls --suite-rebuild
```

## Make sure networking is set/utils available
```
sudo pacman -Syyu
sudo pacman -Sc
sudo pacman-key --refresh-key
sudo pacman -S networkmanager perl-uri
sudo systemctl enable NetworkManager.service
exit
reboot
```

## Install local scripts/setup (as user)
```
cd ~/.bin
./mounting crypt
# again, ssh agent not configured

git submodule update --init
./syncing --install
```

## Locking permissions

Make a link
```
sudo ln -s /home/enck/.bin/locking /usr/local/bin/
```

## Setup the 'core' packages for wm/wireless/utilities/etc.
```
# Make sure keys and cache are all clean/setup
sudo pacman -S alsa-utils chromium feh i3 i3lock i3status dmenu gsfonts lxterminal p7zip pandoc unzip wpa_supplicant xautolock xorg-xdm network-manager-applet cbatticon volumeicon sshfs vinagre base-devel dlang virt-manager cifs-utils

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
touch $HOME/.cache/helper_cache/tmp
cd ~/.bin
./helper_cache rebuild
```

Reboot
