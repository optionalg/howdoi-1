Google Chrome
=============

* Going to use the Fedora/rpm packages for local install
```
sudo pacman -S rpmextract
```

* Extract the download rpm
```
rpmextract <chrome>.rpm
```

* Clean out the old version (if it exists)
```
sudo rm -rf /opt/google/chrome/
```

* Move the necessary bits to the google area
```
mv opt/google/chrome/ /opt/google/
```

* Setup the permissions
```
sudo mv usr/bin/google-chrome-stable /usr/bin/google-chrome-stable
sudo chown root:root /opt/google/chrome/chrome-sandbox
sudo chmod 4755 /opt/google/chrome/chrome-sandbox
```
