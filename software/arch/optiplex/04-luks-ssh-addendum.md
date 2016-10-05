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
wget https://aur.archlinux.org/cgit/aur.git/snapshot/mkinitcpio-dropbear.tar.gz
wget https://aur.archlinux.org/cgit/aur.git/snapshot/mkinitcpio-utils.tar.gz
tar xf mkinitcpio-netconf.tar.gz
tar xf mkinitcpio-dropbear.tar.gz
tar xf mkinitcpio-utils.tar.gz
rm -f *.tar.gz
chown -R enck:enck mkinitcpio*
```

```
su enck
cd mkinitcpio-netconf
makepkg -sri
cd ../mkinitcpio-dropbear
makepkg -sri
cd ../mkinitcpio-utils
makepkg -sri
exit
```

```
cat /home/enck/.ssh/authorized_keys >> /etc/dropbear/root_key
```

```
vim /etc/mkinitcpio.conf
---
# HOOKS change 'encrypt' 'encryptssh' and add 'netconf' and 'dropbear' before 'encryptssh'
```

```
vim /boot/loader/entries/arch-encrypted.conf
---
# add: ip=:::::eth0:dhcp
```
