CrashPlan (frontend) PRO
========================

* Perform the same steps as those for the [backend](https://github.com/enckse/howdoi/blob/master/software/containers/types/crashplan-backend.md)
* Additionally do the following to connect to the backend (which is headless)

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
ssh -L 4200:localhost:[BACKEND PORT] <user>@<backend system>
```

### Notes
---
* The port and token (on the backend) appear to be able to change on restart

### Errors
---

```
# logged via crashplan:
libXtst.so.6: cannot open shared object file: No such file or directory

# resolved:
apt-get install libxtst6
```

```
# logged via crashplan:
libgtk-x11-2.0.so.0: cannot open shared object file: No such file or directory

# resolve:
# debian: apt-get install libswt-gtk-3-java
pacman -S swt
```

Font not rendering text
```
pacman -S gsfonts
```
