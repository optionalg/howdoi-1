## Get started with lxc unprivileged containers (debian)
* Going to need some packages
```
sudo apt-get install lxc uidmap cgmanager
```

* Create this file: /etc/lxc/lxc-usernet
```
    <username> veth lxcbr0 10
```

* Make sure to get the cgroups/unpriv settings set - these 2 items DO NOT persist over reboot
```
sudo sh -c 'echo 1 > /sys/fs/cgroup/cpuset/cgroup.clone_children'
sudo sh -c 'echo 1 > /proc/sys/kernel/unprivileged_userns_clone'
```

* Create a default config for your user: ~/.config/lxc/default.conf
```
    lxc.network.type = veth
    lxc.id_map = u 0 100001 65536
    lxc.id_map = g 0 100001 65536
    lxc.network.link = lxbr0
```

* Define the UIDs/GIDs for usage
```
sudo usermod --add-subuids 100000-165536 <username>
sudo usermod --add-subgids 100000-165536 <username>
```

* Start the container creation process
```
lxc-create -t download -n template
```

