Init systemd-nspawn
---

## machinectl

Required target
```
systemctl enable machines.target
```

Shared networking
```
sudo systemctl edit systemd-nspawn@.service
---
[Service]
ExecStart=
ExecStart=/usr/bin/systemd-nspawn --quiet --keep-unit --boot --link-journal=try-guest --machine=%I
```

