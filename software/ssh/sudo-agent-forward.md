sudo agent forwarding
---

profile script
```
vim /etc/profile.d/sudo-ssh-agent.sh
---
alias sudo-ssh-agent='/etc/conf.d/sudo-ssh-agent.sh'
```

agent forwarding script
```
vim /etc/conf.d/sudo-ssh-agent.sh
---
if [ -z "$SSH_AUTH_SOCK" ]; then
    echo "no agent available..."
    exit -1
fi
sudo su -l -c "export SSH_AUTH_SOCK=$SSH_AUTH_SOCK; /bin/bash;"
```
