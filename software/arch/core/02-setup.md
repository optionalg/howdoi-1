Disk Setup
===

## Array
Make sure any past RAID configs are dropped
```
mdadm --zero-superblock /dev/sdX # and Y
```

Formatting
```
fdisk /dev/sdX # then Y
```
* create a single partition of type (fd) for raid

Create
```
mdadm --create --verbose --level=1 --metadata=1.2 --raid-devices=2 /dev/md0 /dev/sdX1 /dev/sdY1
```

Allow the array to resync as things are still getting set, check progress via
```
cat /proc/mdstat
```

Configure the array then assemble
```
echo 'DEVICE partitions' > /etc/mdadm.conf
mdadm --detail --scan >> /etc/mdadm.conf
mdadm --assemble --scan
```

```
mkdir -p /mnt/Storage
mkdir -p /mnt/Staging
mkdir -p /mnt/Archive
```

follow the addendum for storage, reboot after
```
/sbin/reboot
```

## Make sure networking/dhcp (wired) is available
```
vim /etc/systemd/network/wired.network
---
[Match]
Name=<adapter>

[Network]
DHCP=ipv4
```
```
systemctl enable systemd-networkd
systemctl enable systemd-resolved
systemctl start systemd-networkd
systemctl start systemd-resolved
rm -f /etc/resolv.conf
ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf
```

## LUKS unlock over ssh (dropbear/mkinitcpi-netconf)

We need a user now...
```
useradd -m -s /bin/bash enck
passwd enck
```

```
pacman -S sudo
usermod -G wheel enck
visudo
#uncomment %wheel ALL=(ALL) ALL
```

```
pacman -S wget base-devel
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

need to move our pub key onto the system
```
cp <pub_key> /etc/dropbear/root_key
```

```
vim /etc/mkinitcpio.conf
---
# HOOKS change 'encrypt' 'encryptssh' and add 'netconf' and 'dropbear' before 'encryptssh'
```

```
mkinitcpio -p linux
```

```
vim /etc/default/grub
---
# yes...eth0 not your interface name...it doesn't match
# append to GRUB_CMDLINE_LINUX 'ip=:::::eth0:dhcp'
```

update bootloader and reboot...
```
grub-mkconfig -o /boot/grub/grub.cfg
reboot
```

## Configure ssh
```
pacman -S sshfs openssh rsync
```

## Copy data
```
mkdir -p /tmp/store
sshfs <user>@<ip>:/mnt/Storage /tmp/store
cd /mnt/Storage
rsync -vrziut /tmp/store .
```

## Setup core scripts (bootstrap)
```
cd /opt/
git clone /mnt/Storage/Git/core.git --recursive
cd core
```

setup areas
```
mkdir -p /opt/core/tmp
mkdir -p /opt/core/tmp/repositories
mkdir -p /opt/containers
mkdir -p /opt/containers/shared
mkdir -p /opt/containers/logs
for d in $(echo "cp mail"); do mkdir -p /opt/containers/logs/$d; done
```

iptables
```
ln -s /opt/core/iptables.rules /etc/iptables/iptables.rules
systemctl enable iptables.service
```

containers
```
pacman -S arch-install-scripts
mkdir -p /etc/systemd/nspawn
```

Follow [this](https://github.com/enckse/howdoi/blob/master/software/containers/init-nspawn.md) and either copy archived containers or recreate, make sure they boot

link nspawn files
```
# for each file in /opt/core/systemd-nspawn
ln -s /opt/core/systemd-nspawn/<file> /etc/systemd/nspawn/<name>.nspawn
rm -f /etc/systemd/system/systemd-nspawn\@.service.d/override.conf
ln -s /opt/core/systemd-nspawn/nspawn.override /etc/systemd/system/systemd-nspawn\@.service.d/override.conf
```

helpers
```
curl "https://raw.githubusercontent.com/enckse/home/master/.bin/machinectl-helper" > /usr/local/bin/machinectl-helper
chmod u+x /usr/local/bin/machinectl-helper
```

## Stage data
```
cd core-scripts
mkdir -p /mnt/Staging/Common
./sync-backer.sh staging
./sync-backer.sh archive 
rsync -vrziutc /tmp/store .
```

Reboot
```
/sbin/reboot
```
