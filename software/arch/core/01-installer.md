# Arch Install (core)
---

## Partitioning
fdisk /dev/sdX
```
XXXG - / (83)
YG - swap (82)
```

```
mkfs.ext4 /dev/sdX1
mkswap /dev/sdX2
```

## Mounting file systems
```
mount /dev/sdX1
swapon /dev/sdX2
```

## Package installation (for install)
```
pacstrap /mnt base vim git
```

## Setup fstab
```
genfstab -pU /mnt >> /mnt/etc/fstab
```

Edit and add a line for tmpfs
```
vim /mnt/etc/fstab
---
tmpfs	/tmp	tmpfs	defaults,noatime,mode=1777	0	0
```

## Enter the installing system
```
arch-chroot /mnt /bin/bash
```

## Setup the clock
```
ln -s /usr/share/zoneinfo/<zone_info> /etc/localtime
hwclock --systohc --utc
```

## Set the hostname 
```
echo "<machine>" > /etc/hostname
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

## Set root password
```
passwd
```

## Regen initrd 
```
mkinitcpio -p linux
```

## Grub
```
pacman -S grub
```

```
grub-install --target=i386-pc /dev/sdX
grub-mkconfig -o /boot/grub/grub.cfg
```

## Close up shop and do reboot into installed system
```
exit
umount -R /mnt
swapoff -a
reboot
```
