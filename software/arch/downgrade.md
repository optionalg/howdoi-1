Downgrade (a package)
=====================

Start our work in the pacman cache
```
cd /var/cache/pacman/pkg
```

# Cached?

If it isn't in the package cache...
```
ls -l | grep "<package>"
```

Find the package version in the [archive](https://wiki.archlinux.org/index.php/Arch_Linux_Archive)

```
wget <url to xz archive>
```

# Downgrading

Run package downgrade
```
pacman -U <package>
```

# Ignoring

Add the package names to pacman's config
```
vim /etc/pacman.conf
---
IgnorePkg = <package> <package2>
```

Reference
---

[0] https://wiki.archlinux.org/index.php/downgrading_packages
