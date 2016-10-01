# Arch Install (desktop)
---

## Partitioning
cgdisk /dev/sdX
```
1 500MB EFI partition # hex ef00
2 100% size partiton 
```

Make the necessary file systems
```
mkfs.vfat -F32 /dev/sdX1
```

## LUKS/Encryption setup 
```
cryptsetup -c aes-xts-plain64 -y --use-random luksFormat /dev/sdX2
cryptsetup luksOpen /dev/sdX2 luks
```

## Volume setup for LUKS volumes
```
pvcreate /dev/mapper/luks
vgcreate vg0 /dev/mapper/luks
lvcreate --size 32G vg0 --name swap
lvcreate -l +100%FREE vg0 --name root
```

## File systems on LUKS partition(s) 
```
mkfs.ext4 /dev/mapper/vg0-root
mkswap /dev/mapper/vg0-swap
```

## Mounting file systems
```
mount /dev/mapper/vg0-root /mnt 
swapon /dev/mapper/vg0-swap 
mkdir /mnt/boot
mount /dev/sdX1 /mnt/boot
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

## Configure mkinitcpio for LUKS/boot
```
vim /etc/mkinitcpio.conf
---
# MODULES - add 'ext4'
# HOOKS add 'encrypt' and 'lvm2' before 'filesystems'
```

## Regen initrd 
```
mkinitcpio -p linux
```

## systemd-boot
```
bootctl install
```

```
vim /boot/loader/entries/arch-encrypted.conf
---
title Arch Linux
linux /vmlinuz-linux
initrd /initramfs-linux.img
options cyrptdevice=UUID=</dev/sdX UUID>:vg0 root=/dev/mapper/vg0-root quiet rw ipv6.disable_ipv6=1
```


## Close up shop and do reboot into installed system
```
exit
umount -R /mnt
swapoff -a
reboot
```
