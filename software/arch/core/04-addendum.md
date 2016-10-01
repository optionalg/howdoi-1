Addendum
---

# Encrypt Staging/Archive

LUKS
```
cryptsetup -c aes-xts-plain64 -y --use-random luksFormat /dev/sdXX|YY
cryptsetup luksOpen /dev/sdYY staging
mkfs.ext4 /dev/mapper/staging
cryptsetup luksOpen /dev/sdXX archive
mkfs.ext4 /dev/mapper/archive
```

Setup key
```
dd if=/dev/urandom of=/etc/store.key bs=512 count=8
cryptsetup luksAddKey /dev/sdXX /etc/store.key
cryptsetup luksAddKey /dev/sdYY /etc/store.key
```

Mounting
```
vim /etc/crypttab
---
staging UUID=<lsblk -f YY LUKS>
archive UUID=<lsblk -f XX LUKS>
```

```
vim /etc/fstab
---
/dev/mapper/archive     /mnt/Archive    ext4    defaults    0   0
/dev/mapper/staging     /mnt/Staging    ext4    defaults    0   0
```

```
reboot
```

```
rm -rf /mnt/Archive/lost+found
rm -rf /mnt/Staging/lost+found
```
