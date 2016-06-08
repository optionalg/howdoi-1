Disk Setup
===

## Array
Make sure any past RAID configs are dropped
```
mdadm --zero-superblock /dev/sdX # and Y
```

Formatting
```
fdisk /dev/sdX # then Y
```
* create a single partition of type (fd) for raid

Create
```
mdadm --create --verbose --level=1 --metadata=1.2 --raid-devices=2 /dev/md0 /dev/sdX1 /dev/sdY1
```

Allow the array to resync as things are still getting set, check progress via
```
cat /proc/mdstat
```

Configure the array then assemble
```
echo 'DEVICE partitions' > /etc/mdadm.conf
mdadm --detail --scan >> /etc/mdadm.conf
mdadm --assemble --scan
```

Make the file system
```
mkfs.ext4 /dev/md0
```

Create dir structure
```
mkdir -p /mnt/Storage
mkdir -p /mnt/Staging
mkdir -p /mnt/Archive
```

Setup other disks (single partition)
```
fdisk /dev/sdXX # and YY
mkfs.ext4 /dev/sdXX # and YY
```

Setup fstab
```
vim /etc/fstab
---
# /dev/md0 from by-uuid
UUID=<uuid>     /mnt/Storage    ext4    defaults    0   0

# /dev/sdXX from by-uuid
UUID=<uuid>     /mnt/Archive    ext4    defaults    0   0

# /dev/sdYY from by-uuid
UUID=<uuid>     /mnt/Staging    ext4    defaults    0   0
```

```
mount -a
cd /mnt/Archive # Staging/Storage
rm -rf lost+found
```

Restart
```
/sbin/reboot
```

## Make sure networking/dhcp (wired) is available
```
systemctl enable dhcpcd@<adapter>.service
systemctl start dhcpcd@<adapter>.service
```

## Configure ssh
```
pacman -S sshfs openssh rsync
```

## Copy data
```
mkdir -p /tmp/store
sshfs <user>@<ip>:/mnt/Storage /tmp/store
cd /mnt/Storage
rsync -vrziut /tmp/store .
```

## Setup core scripts (bootstrap)
```
cd /opt/
git clone /mnt/Storage/Git/core.git --recursive
cd core
./manage.sh --install
```

## Stage data
```
cd core-scripts
mkdir -p /mnt/Staging/Common
./sync-backer.sh staging
./sync-backer.sh archive 
rsync -vrziutc /tmp/store .
```

## Create containers
Packages
```
pacman -S screen arch-install-scripts
```

Follow [this](https://github.com/enckse/howdoi/blob/master/software/containers/init-nspawn.md) and either copy archived containers or recreate, make sure they boot

```
machinectl enable <container>
```

Reboot
```
/sbin/reboot
```
