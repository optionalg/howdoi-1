SSMTP
=====
* Mapping entries in /etc/ssmtp/revaliases
```
root:[username]@gmail.com:smtp.gmail.com:587
```

* General config and setting up ssmtp in /etc/ssmtp/ssmtp.conf
```
root=[username]@gmail.com
mailhub=smtp.gmail.com:587
hostname=[username]@gmail.com
UseSTARTTLS=YES
AuthUser=[username]@gmail.com
AuthPass=[password]
FromLineOverride=YES
UseTLS=YES
rewriteDomain=gmail.com
```

* To map local users with a different 'To:' edit /etc/mail.rc
```
alias user user<username@gmail.com>
```

* Test via
```
echo test | mail -v -s "testing ssmtp" <receiving@email.address.com>
```
