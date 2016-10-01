# Arch Install (core)
---

## Partitioning
fdisk /dev/sdX
```
1 1G (83) - bootable
2 100% (83)
```

```
mkfs.ext2 /dev/sdX1
cryptsetup -c aes-xts-plain64 -y --use-random luksFormat /dev/sdX2
cryptsetup luksOpen /dev/sdX2 luks
```

```
pvcreate /dev/mapper/luks
vgcreate vg0 /dev/mapper/luks
lvcreate --size 32G vg0 --name swap
lvcreate -l +100%FREE vg0 --name root
```

```
mkfs.ext4 /dev/mapper/vg0-root
mkswap /dev/mapper/vg0-swap
```

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

## Regen initrd
```
vim /etc/mkinitcpio.conf
---
# MODULES - add 'ext4'
# HOOKS add 'encrypt' and 'lvm2' before 'filesystems'
```

```
mkinitcpio -p linux
```

## Grub
```
pacman -S grub
```

```
vim /etc/default/grub
---
# append to GRUB_CMDLINE_LINUX
cryptdevice=UUID=</dev/sdX1>:vg0
```

```
grub-mkconfig -o /boot/grub/grub.cfg
grub-install --target=i386-pc /dev/sdX
```


## Prep for first boot
```
exit
umount -R /mnt
swapoff -a
reboot
```
