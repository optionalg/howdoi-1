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
sudo mkdir /mnt/Synced
sudo mkdir /mnt/usb
sudo mkdir /mnt/crypt
sudo chown enck:enck /mnt/S*
sudo chown enck:enck /mnt/crypt
```

## Get initial bootstrapping data
```
# Need scp/ssh and rsync for sync'ing
sudo pacman -S openssh rsync

# A place to scp/copy from
sudo vim /etc/hosts
```

* Need to get the copied data locally (via usb from another machine)

## Bootstrap in /tmp
```
cd /tmp
cp /mnt/Synced/crypt.img .
sudo cryptsetup luksOpen--readonly /tmp/crypt.img crypt-tmp
sudo mount /dev/mapper/crypt-tmp /mnt/crypt
```

## Setting up $HOME
```
cd ~
mkdir -p .ssh
cd .ssh/
ln -s /mnt/crypt/ssh/ssh.config config
cd ~
```

## Git setup
```
git init
git remote add origin git@github.com:enckse/home.git
git fetch
git checkout -t origin/master
```

## Reboot
```
sudo /sbin/reboot
```

## Post reboot (as user)
```
cd ~
mkdir Downloads
mkdir .tmp
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
sudo systemctl start NetworkManager.service
/sbin/reboot
```

## Install local scripts/setup (as user)
```
cd ~/.bin
./mounting crypt
# again, ssh agent not configured

# Init local scripts
./nspawn --install
./csv-processing --install
./syncing --install
systemctl start syncing@enck.service
```

## Locking permissions

Make a link
```
sudo ln -s /home/enck/.bin/locking /usr/local/bin/
```
