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
[CrashPlan (backend)](https://github.com/enckse/howdoi/blob/master/software/containers/types/crashplan-backend.md)

[CrashPlan (frontend)](https://github.com/enckse/howdoi/blob/master/software/containers/types/crashplan-frontend.md)

[SSH node/gateway](https://github.com/enckse/howdoi/blob/master/software/containers/types/gateway.md)

[Media management](https://github.com/enckse/howdoi/blob/master/software/containers/types/media.md)