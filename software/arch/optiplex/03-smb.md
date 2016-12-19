samba
===

```
pacman -S samba
```

```
vim /etc/samba/smb.conf
---
[global]
   workgroup = WORKGROUP
   server string = coredesk samba
   log file = /var/log/samba/%m.log
   max log size = 50
   security = user
   dns proxy = no 

[homes]
   comment = Home Directories
   browseable = yes
   writable = yes
```
* make sure 445 is enabled in iptables

```
systemctl restart iptables
systemctl restart smbd
systemctl enable smbd
```

```
useradd --home /home/enck --shell /sbin/nologin zenck
smbpasswd -a zenck
```
