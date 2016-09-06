# User configuration/bootstrapping


## Move into that user
```
su enck
cd ~
mkdir workspace
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
chown -R 755 ~/.synced
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
git pull origin master
ln -s ~/.synced/ssh/config ~/.ssh/config
chmod 600 .ssh/config
git remote remove origin
git remote add origin git@github.com:enckse/home.git
```

## Reboot
```
exit
sudo /sbin/reboot
```

## Post reboot (as user)
```
cd ~
mkdir Downloads
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
dmenu_urls --rebuild
```

## Make sure networking is set/utils available
```
sudo pacman -Syyu
sudo pacman -Sc
sudo pacman-key --refresh-key
sudo pacman -S networkmanager perl-uri
sudo systemctl enable NetworkManager.service
sudo /sbin/reboot
```

## Install local scripts/setup (as user)
```
cd ~/.bin
./mounting crypt
# again, ssh agent not configured

git-sub
./sync --install
```

## Locking permissions

Make a link
```
sudo ln -s /home/enck/.bin/locking /usr/local/bin/
```

Things may not still be working but we're close (don't debug anything _just_ yet)
