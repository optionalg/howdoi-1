CrashPlan (frontend) PRO
========================

* Perform the same steps as those for the [backend](https://github.com/enckse/howdoi/blob/master/software/containers/types/crashplan-backend.md), stopping after CrashPlan's installer has run
* Additionally do the following to connect to the backend (which is headless)

Additional packages
```
pacman -S swt gsfonts
#(select jdk7)
```

Make sure to enable X (if in a container, requires X sharing on the host as well)
```
export DISPLAY=:0
```

As referenced below - ui_info file is found here
```
/var/lib/crashplan/.ui_info
```

Take note of these parts FROM THE BACKEND
```
1234,uuiduuid-uuid-uuid-uuid-uuiduuiduuid,127.0.0.1
PORT, AUTH TOKEN,...
```

Edit the FRONTEND ui_info and replace the PORT with 4200 and AUTH TOKEN with the BACKEND's token. 4200 is just a value that should be free

Create an SSH bridge, notice the use of 4200 (again)
```
ssh -L 4200:localhost:[BACKEND PORT] <user>@<backend system> -4
```

### Notes
---
* The port and token (on the backend) appear to be able to change on restart

