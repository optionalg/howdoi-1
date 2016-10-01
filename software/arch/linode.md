Linode
===
How to install a fully custom and LUKS'd image on linode.

# Bootstrap

1. You will need 2 disk images (1 for bootstrap, 1 for actual install as unformatted/raw)
2. Deploy the Linode arch image (I know, I know) to the bootstrap disk image
3. Follow directions [here](https://www.linode.com/docs/tools-reference/custom-kernels-distros/run-a-distribution-supplied-kernel-with-kvm)

Summarized as install kernel, grub
```
pacman -S linux grub
```

Update grub for linode settings
```
vim /etc/default/grub
---
GRUB_TIMEOUT=10
GRUB_CMDLINE_LINUX="console=ttyS0,19200n8"
GRUB_DISABLE_LINUX_UUID=true
GRUB_SERIAL_COMMAND="serial --speed=19200 --unit=0 --word=8 --parity=no --stop=1"
GRUB_TERMINAL=serial
```

setup grub
```
grub-mkconfig -o /boot/grub/grub.cfg
```

Change the Linode Kernel to "GRUB 2", make sure the raw/unformatted image is attached as well
```
reboot
```

Note: it's possible to lose network here, interface names change during this "update"

# Install

fdisk /dev/sdX (raw/unformatted image
```
1 1G (83) (bootable)
2 100% (83)
```

```
mkfs.ext2 /dev/sdX1
cryptsetup -c aes-xts-plain64 -y --use-random luksFormat /dev/sdX2
cryptsetup luksOpen /dev/sdX2 vps
```

```
pvcreate /dev/mapper/vps
vgcreate vg /dev/mapper/vps
lvcreate --size 1G vg --name swap
lvcreate -l +100%FREE vg --name root
```

```
mkfs.ext4 /dev/mapper/vg0-root
mkswap /dev/mapper/vg0-swap
```

```
mount /dev/mapper/vg-root /mnt
swapon /dev/mapper/vg-swap
mkdir /mnt/boot
mount /dev/sdX1 /mnt/boot
```

# Do the install
```
pacman -S arch-install-scripts
pacstrap /mnt base vim git
```

Setup fstab and move into mnt
```
genfstab -pU /mnt >> /mnt/etc/fstab
# review and remove any entries from /mnt/etc/fstab
# copy anything from the host to the LUKS partition now!
# also a good time to copy the Linode instructed grub changes!
arch-chroot /mnt /bin/bash
```

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

## init
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
# append to GRUB_CMDLINE_LINUX
cryptdevice=UUID=</dev/sdX2>:vg
```

```
grub-mkconfig -o /boot/grub/grub.cfg
```

## Prep for first boot
```
exit
umount -R /mnt
swapoff -a
reboot
```

## Networking

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
