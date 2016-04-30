Power-On-Hours
---

Requires 'smartctl' to be installed

Hours
```
smartctl --all /dev/sd[X] | grep "Power_On_Hours " | tr -s " " | cut -d " " -f 11 | awk '{print $0/1}'
```
* Replace "/1" in awk with "/24" for days or "/8765.81" for years

