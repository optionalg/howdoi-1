Backup
---

Backup to a dir and compressed archive, only keep 30 days worth of data around
```
#!/bin/bash
PHACILITY=/opt/phacility
BACKUP=/opt/backups
GIT_LOCATION=$PHACILITY/git/
UPLOADED=$PHACILITY/files

GIT_SAVE="git"
PHAB=$PHACILITY/phabricator
PHAB_BIN=${PHAB}/bin
CONF_FILES="conf/local/local.json"

TODAY=$(date +%Y-%m-%d-%s)
WRITE_TO=$BACKUP/$TODAY
mkdir -p $WRITE_TO

#sql
$PHAB_BIN/storage dump | gzip > $WRITE_TO/backup.sql.gz

#repositories
for repo in $(ls $GIT_LOCATION); do
	git_out=$WRITE_TO/$GIT_SAVE
	mkdir -p $git_out
	repo_path=$git_out/$repo.tar.gz
	cd $GIT_LOCATION && tar -zcf $repo_path $repo
done

#config file
cd $PHAB && tar -zcf $WRITE_TO/config.tar.gz $CONF_FILES

#uploaded
cd $UPLOADED && tar -zcf $WRITE_TO/uploaded.tar.gz *

#bundle
cd $WRITE_TO && tar -zcf $BACKUP/$TODAY.tar.gz *

#cleanup
find $BACKUP/* -mtime +30 -type f -exec rm {} \;
find $BACKUP -empty -type d -delete
```

[[0]](https://secure.phabricator.com/book/phabricator/article/configuring_backups/)
