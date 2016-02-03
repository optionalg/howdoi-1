### Encrypting

```
# encrypt (using gpg + passphrase) a dir (tar first)
tar -cvzf {name}.tar.gz {directory}/*
gpg -c {name}.tar.gz

# passphrase only, no keyring (gpg2)
gpg --symmetric --cipher-algo aes256 {name}.tar.gz
```

### Decrypting

```
# decrypt gpg -> directory
gpg {name}.tar.gz.gpg


tar xf {name}.tar.gz
```
