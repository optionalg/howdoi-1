Weather
=======

Sending the weather forecast (to myself)

Create a script to execute (e.g. [here](https://github.com/enckse/howdoi/blob/master/software/containers/types/media.md))

Using ssmtp to send it
```
/opt/weather.sh <email> <zip code>
TO=$(cat $FILENAME | grep "^To:" | head -n 1 | cut -d " " -f 2)
ssmtp $TO < $FILENAME
```

