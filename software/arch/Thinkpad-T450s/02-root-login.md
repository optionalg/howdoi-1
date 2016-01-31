# Root login/post install reboot

## Setup a user
```
useradd -m -s /bin/bash enck
passwd enck
```

## Make sure networking/dhcp (wired) is available
```
systemctl enable dhcpcd@enp0s25.service
systemctl start dhcpcd@enp0s25.service
```

## Setup user sudo'ing for wheel, add user to wheel
```
pacman -S sudo
visudo
usermod -G wheel enck
#uncomment %wheel ALL=(ALL) ALL
```
