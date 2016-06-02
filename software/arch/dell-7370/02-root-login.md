# Root login/post install reboot

## Setup a user
```
useradd -m -s /bin/bash enck
passwd enck
```

## Make sure networking/dhcp (wired) is available
```
systemctl enable dhcpcd.service
systemctl start dhcpcd.service
```

## Setup user sudo'ing for wheel, add user to wheel
```
pacman -S sudo
visudo
#uncomment %wheel ALL=(ALL) ALL
usermod -G wheel enck
```

## Blacklist

Blacklist the pc-speaker...
```
echo "blacklist pcspkr" > /etc/modprobe.d/nobeep.conf
```
