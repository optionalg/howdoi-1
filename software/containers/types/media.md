Media management
================
* Can begin with a 'started' container (as root)
* All services/scripts/etc. will run as root
* Requires additional bind(s) to run
* Requires an added systemd-nspawn bind per [core](https://github.com/enckse/core-scripts) scripts

## Scheduling
---

Add the bind (as indicated above)
```
--bind ${MNT_STORAGE}/${ACTIVE} --bind ${RSS_FILES}
```

Install the necessary packages
```
pacman -S git python3 python-pip wget cron rsync zip 
```

Copy media configurations to container
```
cd $HOME
mkdir -p .config
cp <media/file/path>/media .config/
cp <media/file/path>/media-retention .config/
```

Setup 'media-scheduler'
```
cd /opt
git clone https://github.com/enckse/media-scheduler
ln -s /opt/media-scheduler/media-schedule /usr/local/bin/
media-schedule --install
```

Apply additional config files
```
cd $HOME
cp <media/file/path>/rss2email.cfg .config/
mkdir -p .podget
cp <media/file/path>/podgetrc .podget/
cp <media/file/path>/serverlist .podget/
```

Init already 'downloaded' items and/or cache without creating outputs
```
media-schedule --init
```

A quick wrapper to report out errors
```
vim /opt/wrapper.sh
---
#!/bin/bash
logging=/opt/containers/logs/mail/status.log
today=$(date +%Y-%m-%d)
result=$(/usr/local/bin/media-schedule)
if [ ! -z "$result" ]; then
    echo "$today -> $result" >> $logging
fi
```

Defining a weather reporting (via email message)
```
vim /opt/weather.sh
---
#!/bin/bash
DATE=$(date +%Y-%m-%d)
RAN=/var/tmp/weather-$DATE
if [ -e $RAN ]; then
    exit 0
fi
LOCATED=/opt/containers/logs/mail/feed.weather/
mkdir -p $LOCATED
FILENAME="${LOCATED}rss-weather-"$(date +%s)".msg"
mkdir -p $LOCATED
TO=$1
if [ -z $TO ]; then
    echo "missing to field"
    exit -1
fi
ZIP=$2
if [ -z $ZIP ]; then
    echo "missing ZIP code"
    exit -1
fi

echo "To: $TO
Subject: Weather ($DATE)
MIME-Version: 1.0
Content-Type: text/html; charset=\"us-ascii\"
Content-Disposition: inline
" > $FILENAME

curl -A "none" -s http://wttr.in/$ZIP | grep -v "^<a" >> $FILENAME
touch $RAN
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
15 5-12 * * * /opt/weather.sh <email> <zip code>
15 * * * * /opt/wrapper.sh
```

Enable cronie
```
systemctl enable cronie.service
systemctl start cronie.service
```

## Sync
---
* Will be using rsync to do actual sync as shown [here](https://github.com/enckse/home/blob/master/.bin/syncing)
* Requires to be 'booted' for ssh to start/act as a service (systemd-nspawn with '-b')
* Setup as root, SSH'ing is done as non-root
* Make sure a 'normal' user is configured (useradd, chown'd $HOME, etc.)

Make sure sshd is installed
```
pacman -S openssh
```

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
ln -s ${MNT_STORAGE}/${SYNC_FOLDER} Sync
```

## Serving files
---

Create a simple script
```
cd /opt/
echo "python -m http.server 8080" > simple-server.sh
chmod u+x simple-server.sh
```

```
systemctl stop nginx
cd /path/to/files/to/serve
/opt/simple-server.sh
systemctl start nginx
```

## nginx

```
pacman -S nginx
```

```
vim /etc/nginx/nginx.conf
---

#user html;
worker_processes  1;

events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       8080;

        location / {
        root /mnt/Storage/Active/Temp;
            autoindex on;
            index  index.html index.htm;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }
}
```

```
systemctl enable nginx
systemctl start nginx
```
