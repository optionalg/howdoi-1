# User configuration/bootstrapping


## Move into that user
```
su enck
cd ~
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

# Setup git config items
git config --global core.excludesfiles ~/.config/.gitignore
git config --global push.default simple
git config --global core.editor "vim"
git config --global user.name "<name>"
git config --global user.email "<email>"
git config --global core.autocrlf input
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
