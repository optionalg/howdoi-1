#### Install the necessary root DoD certs

Navigate to: http://dodpki.c3pki.chamb.disa.mil/rootca.html, if you view source you'll see links to .p7b files - which is what we need to import

In a 'temp' location 
```
wget http://dodpki.c3pki.chamb.disa.mil/dodeca.p7b
wget http://dodpki.c3pki.chamb.disa.mil/dodeca2.p7b
wget http://dodpki.c3pki.chamb.disa.mil/rel3_dodroot_2048.p7b
```

* Now get them into the actual store
```
for n in *.p7b; do certutil -d sql:$HOME/.pki/nssdb -A -t TC -n $n -i $n; done
```

* The p7b files can be removed now from the 'temp' location

#### Make the CAC reader available
* Run this command (using the libfile for whatever you've setup, this will be using coolkey)
```
modutil -dbdir sql:.pki/nssdb/ -add "CAC Module" -libfile /usr/lib/pkcs11/libcoolkeypk11.so 
```

* Verify the CAC is loaded
```
modutil -dbdir sql:.pki/nssdb/ -list
```

#### References:

[1] https://help.ubuntu.com/community/CommonAccessCard
[2] http://panoptic.com/rking/Getting+DOD+Root+Certificates+working+with+Google+Chrome+under+Linux
