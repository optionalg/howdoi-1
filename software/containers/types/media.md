Media management
================
* Can begin with a 'started' container (as root)
* All services/scripts/etc. will run as root
* Requires additional bind(s) to run
* Requires an added systemd-nspawn bind AND ssmtp setp per [core](https://github.com/enckse/core-scripts) scripts

## Scheduling
---

Add the bind (as indicated above)
```
--bind ${MNT_STORAGE}/${ACTIVE}
```

Install the necessary packages
```
pacman -S ssmtp git python3 python-pip wget cron rsync nginx
```

Configure ssmtp as indicated above
```
vim /etc/ssmtp/revaliases
vim /etc/ssmtp/ssmtp.conf
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

Setting up crontab to handle media scheduling
```
crontab -e
---
30 * * * * /usr/local/bin/media-schedule
```

Enable cronie
```
systemctl enable cronie.service
systemctl start cronie.service
```

## Sync
---
* Follow the [gateway](https://github.com/enckse/howdoi/blob/master/software/containers/types/gateway.md) to setup ssh initially
* Will be using rsync to do actual sync as shown [here](https://github.com/enckse/home/blob/master/.bin/syncing)

Picking up from there, generate a 'sync' ssh key or copy-in existing
```
su enck

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

Setup the nginx config for browsing, notice the root location
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
	    root ${MNT_STORAGE}/${ACTIVE}/Served;
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

Enable/start nginx
```
systemctl enable nginx.service
systemctl start nginx.service
```
