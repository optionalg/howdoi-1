```text
#!/bin/bash
# Create the file (seek is the size that will be produced)
IMG_SIZE=256M
FILE_NAME="encrypted.img"
MAPPER="encrypted-volume"
MNT_TO="$PWD/scratch"
POPULATE_FROM="/mnt/crypt/"
OWNER="enck:enck"

echo "creating image of size $IMG_SIZE"
dd if=/dev/zero of=$FILE_NAME bs=1 count=0 seek=$IMG_SIZE

echo "setting up luks (make sure to respond with uppercase YES)"
sudo cryptsetup luksFormat $FILE_NAME
sudo cryptsetup luksOpen $FILE_NAME $MAPPER

echo "formatting"
sudo mkfs.ext4 /dev/mapper/$MAPPER

echo "mounting"
mkdir -p $MNT_TO
sudo mount /dev/mapper/$MAPPER $MNT_TO

echo "populate from current encrypted image"
sudo chown -R $OWNER $MNT_TO
rsync -vrziut --delete-after $POPULATE_FROM "$MNT_TO/"
read -p "Press [enter] once $MNT_TO has been populated with anything else"
sudo umount $MNT_TO
sudo cryptsetup luksClose $MAPPER
```
