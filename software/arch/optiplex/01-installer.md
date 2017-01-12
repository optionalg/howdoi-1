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
vgcreate vg /dev/mapper/luks
lvcreate --size 32G vg --name swap
lvcreate -l +100%FREE vg --name root
```

## File systems on LUKS partition(s) 
```
mkfs.btrfs /dev/mapper/vg-root
mkswap /dev/mapper/vg-swap
```

## Mounting file systems
```
mount /dev/mapper/vg-root /mnt 
swapon /dev/mapper/vg-swap 
mkdir /mnt/boot
mount /dev/sdX1 /mnt/boot
```

## Package installation (for install)
```
pacstrap /mnt base vim git btrfs-progs
```

## Setup fstab
```
genfstab -pU /mnt >> /mnt/etc/fstab
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
# MODULES - add 'uas' and 'hid-generic'
# HOOKS add 'encrypt' and 'lvm2' before 'filesystems'
```

## Disable pcspkr

```
vim /etc/modprobe.d/nobeep.conf
---
blacklist pcspkr
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
options cryptdevice=UUID=</dev/sdX2 UUID>:vg root=/dev/mapper/vg-root quiet rw 
```

```
cp /boot/loader/entries/arch-encrypted.conf /boot/loader/entries/arch-fallback.conf
vim /boot/loader/entries/arch-fallback.conf
---
# change to
title Arch Linux (fallback)
initrd /initramfs-linux-fallback.img
```

```
vim /boot/loader/loader.conf
---
timeout 3
default arch-encrypted
```

## Close up shop and do reboot into installed system
```
exit
umount -R /mnt
swapoff -a
reboot
```
