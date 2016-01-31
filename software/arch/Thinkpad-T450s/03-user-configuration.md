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
sudo chown enck:enck /mnt/S*
```

## Get initial bootstrapping data
```
# Need scp/ssh and rsync for sync'ing
sudo pacman -S openssh rsync

# A place to scp/copy from
sudo vim /etc/hosts

# Need to get the copied data locally
scp -rp base:/mnt/Storage/Active/Sync/* /mnt/Synced/
```

## Bootstrap in /tmp
```
cd /tmp/
git clone https://github.com/enckse/home
cd home/.bin
# may get warnings about agent
mounting crypt
```

## Setting up $HOME
```
cd ~

# Clone and temporarily setup ssh config information
cd .ssh/
echo "Host github.com
HostName github.com
IdentityFile <path_to_id>
"
cd ~
```

## Git setup
```
git init
git remote add origin git@github.com:enckse/home.git
git fetch
git checkout -t origin/master
cd .nano
git submodule update --init --recursive
```

## Reboot
```
sudo /sbin/reboot
```

## Post reboot (as user)
```
cd ~
mkdir Downloads

# Remove temp config
rm .ssh/config
.bin/mounting crypt

# Setup 'real' ssh.config
ln -s <path_to_real>/ssh.config .ssh/config

# Verify host key for sync service (later)
ssh sync

# Setup git config items
git config --global core.excludesfiles ~/.config/.gitignore
git config --global push.default simple
git config --global core.editor "vim"
git config --global user.name "<name>"
git config --global user.email "<email>"
```

## Make sure networking is set/utils available
```
sudo pacman -S nfs-utils networkmanager perl-uri
sudo systemctl enable NetworkManager.service
sudo systemctl start NetworkManager.service
/sbin/reboot
```

## Install local scripts/setup
```
cd ~/.bin
mounting crypt

# Init local scripts
nspawn --install
csv-processing --install
syncing --install
```

## Locking permissions

Make a link
```
sudo ln -s /home/enck/.bin/locking /usr/local/bin/
```
