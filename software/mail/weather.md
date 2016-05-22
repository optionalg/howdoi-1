Weather
=======

Sending the weather forecast (to myself)

Create a script to execute
```
vim weather.sh
---
#!/bin/bash
DATE=$(date +%Y-%m-%d)
LOCATED=/tmp/
FILENAME="${LOCATED}weather-"$(date +%s)".html"
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

curl -A "none" -s http://wttr.in/$ZIP >> $FILENAME
ssmtp $TO < $FILENAME
```

Make sure it is executable
```
chmod u+x weather.sh
```

Run it with email and zip as the arguments
```
./weather.sh <to> <zip>
```
