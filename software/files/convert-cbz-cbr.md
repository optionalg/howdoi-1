# CBR/CBZ conversion

Remove whitespace from file names
```
ls | while read -r FILE; do     mv -v "$FILE" `echo $FILE | tr ' ' '_' | tr -d '[{}(),\!]' | tr -d "\'" | tr '[A-Z]' '[a-z]' | sed 's/_-_/_/g'`; done
```

Unpack, transform, and compose
```
#!/bin/bash

FILE=$1
NAME=$2
if [ -z "$FILE" ]; then
    echo "File is required..."
    exit -1
fi

if [ ! -e "$FILE" ]; then
    echo "$FILE does not exist..."
    exit -1
fi

if [ -z "$NAME" ]; then
    echo "Name is required..."
    exit -1
fi

if [ -d "$NAME" ]; then
    echo "$NAME already exists..."
    exit -1
fi

function is_file_type()
{
    echo $1 | grep -q "\.$2$"
    if [ $? -eq 0 ]; then
        echo 0
    else
        echo 1
    fi
}

is_cbr=$(is_file_type "$FILE" "cbr")
is_cbz=$(is_file_type "$FILE" "cbz")

if [ $is_cbr -eq 1 ] && [ $is_cbz -eq 1 ]; then
    echo "unknown file type"
    exit -1
fi

mkdir -p $NAME
if [ $is_cbr -eq 0 ]; then
    unrar e "$FILE" $NAME
fi

if [ $is_cbz -eq 0 ]; then
    unzip "$FILE" -d $NAME
fi

first=0
echo "" > $NAME.md
find $NAME/ -type f -iname "*.jpg" -print0 | sort -z | while IFS= read -r -d '' file; do
    echo "![]($file)" >> $NAME.md
done
pandoc $NAME.md -o $NAME.pdf
rm -f $NAME.md
rm -rf $NAME/
```
