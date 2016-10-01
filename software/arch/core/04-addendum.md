Addendum
---

# Encrypt Staging/Archive

LUKS
```
cryptsetup -c aes-xts-plain64 -y --use-random luksFormat /dev/md0|sd(XX|YY)
cryptsetup luksOpen /dev/md0 store
mkfs.ext4 /dev/mapper/store
cryptsetup luksOpen /dev/sdYY staging
mkfs.ext4 /dev/mapper/staging
cryptsetup luksOpen /dev/sdXX archive
mkfs.ext4 /dev/mapper/archive
```

Setup key
```
dd if=/dev/urandom of=/etc/store.key bs=512 count=8
cryptsetup luksAddKey /dev/md0 /etc/store.key
cryptsetup luksAddKey /dev/sdYY /etc/store.key
cryptsetup luksAddKey /dev/sdXX /etc/store.key
```

Mounting
```
vim /etc/crypttab
---
store   UUID=<lsblk -f md0 crypto> /etc/store.key
staging UUID=<lsblk -f YY LUKS>    /etc/store.key
archive UUID=<lsblk -f XX LUKS>    /etc/store.key
```

```
vim /etc/fstab
---
/dev/mapper/archive     /mnt/Archive    ext4    defaults    0   0
/dev/mapper/staging     /mnt/Staging    ext4    defaults    0   0
/dev/mapper/store       /mnt/Storage    ext4    defaults    0   0
```

```
reboot
```

```
rm -rf /mnt/Storage/lost+found
rm -rf /mnt/Staging/lost+found
rm -rf /mnt/Archive/lost+found
```
