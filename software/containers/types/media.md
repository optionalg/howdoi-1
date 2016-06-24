Media management
================
* Requires additional bind(s) to run (for syncing/hosting/storage)

## Scheduling
---

Install the necessary packages
```
pacman -S git python3 python-pip cron rsync nginx openssh
```

Make necessary dirs/files
```
cd $HOME
mkdir -p .config
mkdir -p .upodder
mkdir -p .local/share
mkdir -p .cache/
cp <media/file/path>/media .config/
cp <media/file/path>/rss2email.cfg .config/
cp <media/file/path>/subscriptions .upodder/
```

Setup utililities
```
cd /opt
git clone https://github.com/enckse/rss2email.git r2e
cd r2e
pip3 install feedparser html2text upodder
python setup.py install
ln -s /opt/r2e/r2e /usr/local/bin/
```

Workaround [this](https://github.com/m3nu/upodder/issues/16)
```
vim /usr/lib/python3.5/site-packages/upodder/upodder.py
---
# change .DEBUG -> .ERROR
```

Init already 'downloaded' items and/or cache without creating outputs
```
r2e run --no-send
upodder --no-download
upodder --mark-seen
```

A quick wrapper to report out errors
```
vim /opt/wrapper.sh
---
[INSERT SCRIPT]
```

Defining a weather reporting (via email message)
```
vim /opt/weather.sh
---
[INSERT SCRIPT]
```

And executable bit for both
```
chmod u+x /opt/wrapper.sh
chmod u+x /opt/weather.sh
```

Setting up crontab to handle scheduling
```
crontab -e
---
[CRONTAB]
```

Enable cronie
```
systemctl enable cronie.service
systemctl start cronie.service
```

## Sync
---
* Will be using rsync to do actual sync as shown [here](https://github.com/enckse/home/blob/master/.bin/syncing)
* Setup as root, SSH'ing is done as non-root
* Make sure a 'normal' user is configured (useradd, chown'd $HOME, etc.)

Edit/modify these settings to validate/verify proper config

```
vim /etc/ssh/sshd_config
---
Port <desired>

PermitRootLogin no

AuthorizedKeysFile    %h/.ssh/authorized_keys

PasswordAuthentication no
```

Using a 'regular' user so make sure it is set before entering as them

```
su <user> 
```

Configure ssh private key auth for the user
```
cd ~
mkdir .ssh
chmod 700 .ssh

#<copy key(s) to authorized_keys>
chmod 600 authorized_keys

# leave user context
exit
```

Start/enable the service
```
systemctl enable sshd
systemctl start sshd
```

Generate a 'sync' ssh key or copy-in existing
```
su <user> 

# or generate
ssh-keygen -t rsa -b 4096 -C "<email>"
```

Create a link (as user)
```
cd ~
ln -s ${MNT_STORAGE}/Home/Synced Sync
```

## nginx

```
vim /etc/nginx/nginx.conf
---
[INSERT CONF]
```

```
openssl passwd
```

```
vim /etc/nginx/htpasswd
---
<user>:<pass>
```

```
systemctl enable nginx
systemctl start nginx
```
