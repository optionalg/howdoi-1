ubnt serial
===

```
pacman -S minicom
```

```
sudo minicom -s
```

Select "Serial port setup"
verify that:
```
Device: /dev/ttyUSB0
Baud: 115200
HW: Off
```

Select "Save setup as dfl" and exit

```
sudo minicom
```

Using minicom
```
Ctrl-A then Z -> Help
Ctrl-A then M -> Init modem
```

* Takes time to load, it should prompt for user/pass

```
> ? (for help)
> enable (to get into 'normal' ubnt shell)
```

```
# ?
# help
# exit

```

```
> exit
```

[ubnt](https://help.ubnt.com/hc/en-us/articles/205202630-EdgeMAX-Connect-to-serial-console-port-default-settings)
[arch wiki](https://wiki.archlinux.org/index.php/working_with_the_serial_console)
