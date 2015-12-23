# encrypt (using gpg + passphrase) a dir (tar first)
tar -cvzf {name}.tar.gz {directory}/*
gpg -c {name}.tar.gz

# decrypt gpg -> directory
gpg {name}.tar.gz.gpg
tar xf {name}.tar.gz
