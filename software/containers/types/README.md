Containers
==========

Layout of how/what can be done for some systemd-nspawn container definitions from a base 'template' container definition in Arch

## Common
---
* Update '/etc/hosts' with the machine/container name
```
vim /etc/hosts
---
127.0.1.1   <name>.<domain>   <name>
```

* Enable root login on pts/0 (or more) as needed
```
vim /etc/securetty
---
# append
pts/0
```

* Make sure everthing is up-to-date
```
pacman -Syyu
```

## Systems
---
[CrashPlan (backend)](crashplan-backend.md)

[CrashPlan (frontend)](crashplan-frontend.md)

[Media management](media.md)
