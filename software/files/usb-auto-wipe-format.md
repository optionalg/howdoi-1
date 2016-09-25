USB auto zero/format
===

```
#!/bin/bash
"Provides a script to monitor for USB disk drives to
1. wipe
2. partition (label)
3. format

when they are plugged in (keeping track of disks it has already done)
"
MATCH="/dev/disk/by-id/usb-*"
STORE="/tmp/usb-formatter.cache"
TMP_STORE="/tmp/usb-formatter.tmp"
FORCE_KEY="--force"
HELP_KEY="--help"
NOFORMAT_KEY="--no-format"
NOWIPE_KEY="--no-wipe"
NOPART_KEY="--no-partition"
DRYRUN_KEY="--dry-run"
TEMPLATE_DEV="DEVICE:NAME"
WIPE="dd if=/dev/zero of=$TEMPLATE_DEV"
LABEL="parted $TEMPLATE_DEV --script -- mklabel msdos"
PARTITION="parted $TEMPLATE_DEV --script -- mkpart primary 0 -1"
FORMAT="mkfs.vfat $TEMPLATE_DEV"
ON=1
OFF=0

function run-enabled()
{
    if [ $1 -eq $ON ]; then
        echo $5" -> "$2
        if [ $3 -eq $OFF ]; then
            $4
            sleep 1
        fi
    fi
}

function process-usb()
{
    run-enabled $2 "wipe" $5 "dd if=/dev/zero of=$1" $1
    run-enabled $3 "label" $5 "parted $1 --script -- mklabel msdos" $1
    run-enabled $3 "partition" $5 "parted $1 --script -- mkpart primary 0 -1" $1
    run-enabled $4 "format" $5 "mkfs.vfat ${1}1" $1
}

function run()
{
    rm -f $TMP_STORE
    touch $TMP_STORE
    touch $STORE
    do_work=""
    if ls $MATCH 1> /dev/null 2>&1; then
        do_work="true"
    fi
    if [ ! -z "$do_work" ]; then
        echo "found disks to format"
        proc $@
    fi
    if [ $4 -eq 0 ]; then
        mv $TMP_STORE $STORE
    else
        rm -f $TMP_STORE
    fi
}

function proc()
{
    for matched in $(ls $MATCH); do
        link=$(readlink -f $matched)
        echo $link | grep -v -q "[0-9]\+"
        if [ $? -eq 0 ]; then
            echo "matched: $link ($matched)"
            echo $matched >> $TMP_STORE
            cat $STORE | grep -q "$matched"
            if [ $? -ne 0 ] || [ $5 -eq $ON ]; then
                process-usb $link $@
            else
                echo "$link -> no-op"
            fi
        fi
    done
}

args=$@
wipe=$ON
part=$ON
format=$ON
dryrun=$OFF
force=$OFF
if [ ! -z $1 ]; then
    for arg in $args; do
        case $arg in
            $DRYRUN_KEY)
                dryrun=$ON
                ;;
            $NOPART_KEY)
                part=$OFF
                format=$OFF
                ;;
            $NOFORMAT_KEY)
                format=$OFF
                ;;
            $NOWIPE_KEY)
                wipe=$OFF
                ;;
            $FORCE_KEY)
                force=$ON
                ;;
            $HELP_KEY | *)
                echo "usage:
    $DRYRUN_KEY - dryrun only, no actions executed
    $NOPART_KEY - do not partition (or format)
    $NOFORMAT_KEY - do not format
    $NOWIPE_KEY - do not wipe
                "
                if [[ $args == "$HELP_KEY" ]]; then
                    exit 0
                else
                    exit -1
                fi
                ;;
        esac
    done
fi

run $wipe $part $format $dryrun $force
```
