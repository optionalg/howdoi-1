Media management
================
* Requires additional bind(s) to run (for syncing/hosting/storage)

## Scheduling
---

Install the necessary packages
```
pacman -S git python3 python-pip cron rsync openssh
```

Make necessary dirs/files
```
cd $HOME
mkdir -p .config
mkdir -p .local/share
mkdir -p .cache/
cp <media/file/path>/media .config/
cp <media/file/path>/rss2email.cfg .config/
```

Setup utililities
```
cd /opt
git clone https://github.com/enckse/rss2email.git r2e
cd r2e
pip3 install feedparser html2text
python setup.py install
ln -s /opt/r2e/r2e /usr/local/bin/
```

Init already 'downloaded' items and/or cache without creating outputs
```
r2e run --no-send
```

A quick wrapper to report out errors
```
vim /opt/wrapper.sh
---
#!/bin/bash
source $HOME/.config/media
mail_out=/opt/containers/logs/mail/
status_file=${mail_out}status.log
today=$(date +%Y-%m-%d)
located=${mail_out}feed.weather/
weather_ran=/var/tmp/weather-$today
function report()
{
    if [ ! -z "$1" ]; then
        echo "$today -> $1" >> $status_file
    fi
}

function get-weather()
{
     if [ -e $weather_ran ]; then
        exit 0
     fi
     mkdir -p $located
     FILENAME="${located}rss-weather-"$(date +%s)".msg"

    echo "To: $WEATHER
Subject: Weather ($today)
MIME-Version: 1.0
Content-Type: text/html; charset=\"us-ascii\"
Content-Disposition: inline
" > $FILENAME

    curl -A "none" -s http://wttr.in/$ZIP | grep -v "^<a" >> $FILENAME
    touch $weather_ran
}

case $1 in
    "weather")
        res=$(get-weather 2>&1)
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
            res=$(r2e run $r 2>&1)
            report $res
        done
        ;;
esac
```

executable bit
```
chmod u+x /opt/wrapper.sh
```

Setting up crontab to handle scheduling
```
crontab -e
---
15 5-12 * * * /opt/wrapper.sh weather
15 8,11,14,17,20 * * * /opt/wrapper.sh rss
15 12,18 * * * /opt/wrapper.sh rss bi-daily
15 19 * * * /opt/wrapper.sh rss daily
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
