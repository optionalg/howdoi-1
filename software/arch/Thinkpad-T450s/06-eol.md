Closing up
==========

Stop syncing
```
sudo systemctl stop syncing@enck.service
sudo systemctl disable syncing@enck.service
```

Send tar cached files
```
cd ~/.cache
tar cf archive.tar background.png demu_urls/*.index nspawn/* ssh.jumps
scp archive.tar base:~/
```
