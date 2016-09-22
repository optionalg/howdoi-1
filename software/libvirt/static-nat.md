static nat
===

Assumes using dnsmasq and ebtables for NAT'd networking on child VMs on the host. Also that we're only using dnsmasq for this purpose

* first make sure dnsmasq starts and binds only how we want
```
vim /etc/dnsmasq.conf
---
interface=name
# or listen-address=ip
# and
bind-interfaces
```

* start a 'virsh' session
```
# virsh commands, assumes 'default' config name
net-edit default
```

* add an entry after the dhcp/range path
```
<host mac='mac-address' name='vm-name' ip='static-ip' />
```

* back to 'virsh' session
```
net-destroy default
net-start default
```

* Should reboot the host just to pick everything up
```
reboot
```

# References
[0] - http://wiki.libvirt.org/page/Libvirtd_and_dnsmasq
[1] - http://www.cyberciti.biz/faq/linux-kvm-libvirt-dnsmasq-dhcp-static-ip-address-configuration-for-guest-os/
