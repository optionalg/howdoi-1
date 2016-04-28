# Root login/post install reboot

## Setup a user
```
useradd -m -s /bin/bash enck
passwd enck
```

## Make sure networking/dhcp (wired) is available
```
systemctl enable dhcpcd@<adapter>.service
systemctl start dhcpcd@<adapter>.service
```

## Setup user sudo'ing for wheel, add user to wheel
```
pacman -S sudo
usermod -G wheel enck
visudo
#uncomment %wheel ALL=(ALL) ALL
```

## Networking utilities
```
pacman -S openssh wget
```

# User configuration/bootstrapping


## Move into that user
```
su enck
cd ~
rm .bash*
```

## Configure git
```
git config --global core.excludesfiles ~/.config/.gitignore
git config --global push.default simple
git config --global core.editor "vim"
git config --global user.name "<name>"
git config --global user.email "<email>"
git config --global core.autocrlf input
```

## Bash profile
```
wget https://raw.githubusercontent.com/enckse/home/master/.bash_profile
wget https://raw.githubusercontent.com/enckse/home/master/.bashrc
cat .bashrc | head -n 60 > .bashrc.tmp
mv .bashrc.tmp .bashrc
wget https://raw.githubusercontent.com/enckse/home/master/.vimrc
```
