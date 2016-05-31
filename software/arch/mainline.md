linux-mainline (aur)
===

Build packages
```
sudo pacman -S --needed base-devel
```

Working area
```
sudo mkdir /opt/kernel
sudo chown enck:enck /opt/kernel
cd /opt/kernel
```

Retrieve, build, and install
```
curl -L -O http://aur.archlinux.org/cgit/aur.git/snapshot/linux-mainline.tar.gz
tar -xvf linux-mainline.tar.gz
cd linux-mainline
makepkg -sri
sudo pacman -U linux-mainline-*.tar.xz
```

Add a loader (make sure the default is set properly in /boot/loader/loader.conf)
```
vim /boot/loader/entries/arch-mainline.conf
---
title Arch Linux (mainline)
linux /vmlinuz-linux-mainline
initrd /initramfs-linux-mainline.img
options cryptdevice=UUID=<drive_uuid>:vg0 root=/dev/mapper/vg0-root quiet rw
```

Reboot!
