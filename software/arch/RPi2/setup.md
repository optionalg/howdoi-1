# Arch Install (Raspberry Pi 2)
---

## Prep the Pi2/SD

From another machine - fdisk the SD card
```
fdisk /dev/sdX
---
commands:
o # or 'd', deleting partitions
n, p, 1, +100M # new partition for boot
t, c # FAT32 partition
n, p, 2, <enter> # new partition for root
w # save to disk
```

Create the file systems and mount (requires dosfstools)
```
mkfs.vfat /dev/sdX1
mkfs.ext4 /dev/sdX2
mkdir boot
mkdir root
mount /dev/sdX1 boot
mount /dev/sdX2 root
```

Get and copy the image to the proper locations
```
wget http://os.archlinuxarm.org/os/ArchLinuxARM-rpi-2-latest.tar.gz
bsdtar -xpf ArchLinuxARM-rpi-2-latest.tar.gz -C root
sync
mv root/boot/* boot
umount boot/ root/
```

Can now boot the SD card in the Pi 2 (logins are alarm/alarm or root/root)

## From the RPi2 and/or SSH'ing in

## Setup the clock
```
rm /etc/localtime
ln -s /usr/share/zoneinfo/<zone_info> /etc/localtime
```

## Set the hostname 
```
echo "<machine>" > /etc/hostname
```

## Install packages
```
pacman -Syyu
pacman -S vim sudo
```

## Locale setup
```
vim /etc/locale.gen
---
# uncomment en_US.UTF-8 UTF-8 and/or others
# then run
locale-gen
```

## Set locale LANG
```
echo LANG=en_US.UTF-8 >> /etc/locale.conf
```

## Add user
```
useradd enck
mkdir /home/enck
chown enck:enck /home/enck
```

## Set root password
```
passwd
/sbin/reboot
```

## Configure sudo
```
visudo
# uncomment
# %wheel ALL=(ALL) ALL
```

modify the user
```
usermod -G wheel -s /bin/bash enck
```

drop the 'alarm' user
```
userdel alarm
```

## Adjust SSH
```
vim /etc/ssh/sshd_config
---
PermitRootLogin no
PasswordAuthentication no
```

```
systemctl restart sshd
```

```
su enck
cd ~
mkdir .ssh
chmod 700 .ssh
cd .ssh
#<copy key>
chmod 600 authorized_keys
```

## Swap
```
fallocate -l 1024M /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo 'vm.swappiness=1' > /etc/sysctl.d/99-sysctl.conf
```

```
vim /etc/fstab
---
/swapfile none swap defaults 0 0
```

## Disable tmpfs
```
systemctl stop tmp.mount
systemctl disable tmp.mount
```
