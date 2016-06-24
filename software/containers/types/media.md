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
#!/bin/bash
source $HOME/.config/media
status_file=/opt/containers/logs/mail/status.log
podcast_dir=/mnt/Storage/Active/Temp/podcasts/
today=$(date +%Y-%m-%d)
function report()
{
    if [ ! -z "$1" ]; then
        echo "$today -> $1" >> $status_file
    fi
}

mkdir -p $podcast_dir
find $podcast_dir* -mtime +30 -type f -exec rm {} \;
find $podcast_dir -empty -type d -delete
case $1 in
    "podcasts")
        store=$podcast_dir$today
        mkdir -p $store
        res=$(upodder --podcastdir $store)
        report "$res"
        ;;
    "rss")
        daily="-v"
        bi="-v"
        case $2 in
            "daily")
                daily=""
                ;;
            "bi-daily")
                bi=""
                ;; 
     	esac
        for r in $(r2e list | grep $daily -E "$DAILY_FEEDS" | grep $bi -E "$BI_DAILY_FEEDS" | cut -d ":" -f 1); do
            res=$(r2e run --no-send $r)
            report $res
        done
        ;;
esac
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
15 5-12 * * * /opt/weather.sh enckse+weather@gmail.com 48073
15 8,11,14,17,20 * * * /opt/wrapper.sh rss
15 12,18 * * * /opt/wrapper.sh rss bi-daily
15 19 * * * /opt/wrapper.sh rss daily
15 23 * * * /opt/wrapper.sh podcasts
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
            auth_basic "closed site";
            auth_basic_user_file htpasswd;
            root /mnt/Storage/Active/Temp;
            autoindex on;
            index  index.html index.htm;
        }

	location /shared {
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
