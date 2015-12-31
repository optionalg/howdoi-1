Pantum P2500w
=============

Requires having the Linux rar drivers already - this is aimed at Debian

```
PRINTER_RAR=20150520PantumP2200-P2500-Linux-v1.70.rar
PRINTER_TAR=LinuxInstall20150410.tar.gz

# packages required and services started
sudo apt-get install cups unrar
sudo systemctl start cups

# unpack
unrar e $PRINTER_RAR
tar xzvf $PRINTER_TAR

# move resources and set them up
cd LinuxInstall/Resources
dpkg-deb -R Pantum-P2500-Series-2.5.x86_64.deb .
sudo mv ./usr/lib/cups/filter/pt2500Filter /usr/lib/cups/filter/
sudo chown root:root /usr/lib/cups/filter/pt2500Filter
sudo mkdir -p /usr/share/cups/model/Pantum
sudo mv ./usr/share/cups/model/Pantum/* /usr/share/cups/model/Pantum

# manual intervention
echo "navigate to http://localhost:631/admin/"
echo "add printer"
echo "select the pantum discovered"
echo "select the 2500w ppd from the /usr/share/cups/model/Pantum location"

# cleanup
rm $PRINTER_TAR
rm -rf LinuxInstall*
```
