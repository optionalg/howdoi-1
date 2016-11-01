# Arch Install (Dell 7370)
---

## Start networking
```
systemctl start dhcpcd.service

```

## Partitioning
cgdisk /dev/sdb
```
1 1GB EFI partition # hex ef00
2 100% size partiton 
```

Make the necessary file systems
```
mkfs.vfat -F32 /dev/sdb1
```

## LUKS/Encryption setup 
```
cryptsetup -c aes-xts-plain64 --key-size 512 --hash sha512 -y --use-random luksFormat /dev/sdb2
cryptsetup luksOpen /dev/sdb2 luks
```

## Volume setup for LUKS volumes
```
pvcreate /dev/mapper/luks
vgcreate vg /dev/mapper/luks
lvcreate --size 8G vg --name swap
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
mount /dev/sdb1 /mnt/boot
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
# if you want keyboard :/
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
options cryptdevice=UUID=</dev/sdb2 UUID>:vg root=/dev/mapper/vg-root quiet rw
```

```
vim /boot/loader/loader.conf
---
# uncomment and change
timeout 1
```


## Close up shop and do reboot into installed system
```
exit
umount -R /mnt
swapoff -a
reboot
```
