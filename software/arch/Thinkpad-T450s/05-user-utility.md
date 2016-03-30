# User Utility/Helpers

## Necessary packages
```
sudo pacman -S keepassx2 bash-completion pang arch-install-scripts rfkill cronie rpmextract gconf vim-supertab redshift
```

## Bash auto-complete
```
sudo ln -s /home/enck/.bin/autocomplete/* /usr/share/bash-completion/completions/
```

## Workspace/container setup
```
sudo mkdir /opt/workspace
sudo mkdir /opt/workspace/containers
cd /opt/workspace/containers
mkdir template
sudo pacstrap -i -c -d template/ base
cd ~
mkdir /opt/workspace/container-bin
mkdir /opt/workspace/shared
ln -s /opt/workspace/shared/ workspace
```

## Disable bluetooth
```
sudo systemctl enable rfkill-block@bluetooth.service
sudo systemctl start rfkill-block@bluetooth.service
```

## Chrome (google-chrome)
Use rpmextract + google chrome rpm to extract and then put each item in it's proper place. Chrome, at this point, will require gconf

## CAC reader
```
sudo pacman -S ccid opensc
```

```
sudo vim /etc/opensc.conf
---
# comment in enable_pinpad = false (2 places)
```

```
sudo systemctl enable pcscd.service
sudo systemctl start pcscd.service
```

Enable wget
```
sudo pacman -S wget
```

Follow instructions from [here](https://github.com/enckse/howdoi/blob/master/software/chrome/dod-certs.md)

## File Management
```
# xclip for cli > clipboard, rox for basic fm, tree for output of image structure
sudo pacman -S xclip rox tree
```
