ssh_config
===

* "Match" rules
```
vim ~/.ssh/config
---
Match exec "echo '%n' | grep -q -E '^(host1|host2|host3)$'"
    Port 1234

Match exec "echo '%n' | grep -q -E '^(host1|host2)$'"
    ForwardAgent yes
```

* Proxy through
```
vim ~/.ssh/config
---
Host proxy
    HostName proxy.example.com
    RequestTTY force
    LocalCommand ssh dest.example.com
    PermitLocalCommand yes
```
