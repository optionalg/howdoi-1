#### Install the necessary root DoD certs

Navigate to http://iase.disa.mil/pki-pke/Pages/tools.aspx

Go to "Trust Store" and down to the "PKI CA Certificate Bundles: PKCS#7" section, download the "For DoD PKI Only - Version 5.0" zip

In a temp location
```
unzip Certificates_PKCS7_v5.0u1_DoD.zip
cd Certificates_PKCS7_v5.0u1_DoD
for n in (ls * | grep Chrome); do certutil -d sql:$HOME/.pki/nssdb -A -t TC -n $n -i $n; done
```

* The p7b files can be removed now from the 'temp' location

#### Make the CAC reader available
* Run this command (using the libfile for whatever you've setup, this will be using coolkey in Debian, opensc in Arch), from $HOME
```
cd $HOME
# use libcoolkeypk11.so for Debian
modutil -dbdir sql:.pki/nssdb/ -add "CAC Module" -libfile /usr/lib/pkcs11/opensc-pkcs11.so 
```

* Verify the CAC is loaded
```
modutil -dbdir sql:.pki/nssdb/ -list
```

#### References:

[1] https://help.ubuntu.com/community/CommonAccessCard
[2] http://panoptic.com/rking/Getting+DOD+Root+Certificates+working+with+Google+Chrome+under+Linux
