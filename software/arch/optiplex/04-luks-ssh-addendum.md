LUKS + SSH
===

make sure we're up-to-date
```
pacman -Sc
pacman-key --refresh-keys
pacman -Syyu
```

as root, get resources
```
pacman -S base-devel
cd /opt
wget https://aur.archlinux.org/cgit/aur.git/snapshot/mkinitcpio-netconf.tar.gz
wget https://aur.archlinux.org/cgit/aur.git/snapshot/tinyssh.tar.gz
wget https://aur.archlinux.org/cgit/aur.git/snapshot/ucspi-tcp.tar.gz
wget https://aur.archlinux.org/cgit/aur.git/snapshot/mkinitcpio-tinyssh.tar.gz
wget https://aur.archlinux.org/cgit/aur.git/snapshot/mkinitcpio-utils.tar.gz
tar xf mkinitcpio-netconf.tar.gz
tar xf mkinitcpio-utils.tar.gz
tar xf mkinitcpio-tinyssh.tar.gz
tar xf tinyssh.tar.gz
tar xf ucspi-tcp.tar.gz
rm -f *.tar.gz
chown -R enck:enck mkinitcpio*
```

```
su enck
# needed as of (2016-10-31)
gpg --keyserver hkp://pgp.mit.edu --recv-keys 0x45DA517496939FF9
cd mkinitcpio-netconf
makepkg -sri
cd tinyssh
makepkg -sri
ccd ucspi-tcp
makepkg -sri
cd ../mkinitcpio-tinyssh
makepkg -sri
cd ../mkinitcpio-utils
makepkg -sri
exit
```

```
cat /home/enck/.ssh/authorized_keys >> /etc/tinyssh/root_key
```

```
vim /etc/mkinitcpio.conf
---
# HOOKS change 'encrypt' 'encryptssh' and add 'netconf' and 'tinyssh' before 'encryptssh'
```

```
vim /boot/loader/entries/arch-encrypted.conf
---
# add: ip=:::::eth0:dhcp
```
