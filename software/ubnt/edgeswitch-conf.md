EdgeSwitch Config Backup
===

Pull a config from an edgeswitch via bash/expect/screen. This solution is not fully guaranteed though the concepts, if tweaked, should work

# bash

Assume using 'pass' to get passwords (using alias for pass optionally)
```
vim get-configs
---
#!/bin/bash
pass_offset="pass/offset/for/creds/"
if [ ! -z "$1" ]; then
    export PASSWORD_STORE_DIR=$1
    export PASSWORD_STORE_GIT=$1
fi

for srv in $(echo "server1 server2 serverN"); do
    use_pass=$(pass show ${pass_offset}$srv)
    expect run-ssh-pull $use_pass $srv
done
```

# expect

requires 'expect', host key should be accepted (or adjust ssh command below), change ssh settings as needed
```
vim run-ssh-pull
---
#!/usr/bin/expect
set pass [lindex $argv 0]
set server [lindex $argv 1]
spawn ssh $server
expect "password:"
send "$pass\n"
expect ">"
send "en\n"
expect "Password:"
send "$pass\n"
expect "#"
send "show running-config\n"
expect "More"
send "1000d\n"
expect "More"
send "q\n"
expect "#"
send "exit\n"
expect ">"
send "exit\n"
interact
```

# screen

to log the results
```
screen -L -dm -S pull-configs /bin/bash ./get-configs
```
