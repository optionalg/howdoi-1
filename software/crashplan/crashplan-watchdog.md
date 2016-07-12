CrashPlan (watchdog)
====================
Used to watch crashplan and make sure it doesn't stay stopped for long, logs any 'problems' and gives crashplan a time window to 'recover'
```
vim /opt/crashplan-watcher
---
#!/bin/bash
WATCHDOG_BASE="/opt/containers/logs/cp/"
WATCHDOG_FILE="${WATCHDOG_BASE}cp.watchdog"
TODAY=$(date +%m/%d/%y)
WATCHDOG_LOG="${WATCHDOG_BASE}watchdog.log"
NOW=$(date +%s)
ERROR_BOUND=5400
touch $WATCHDOG_LOG
function report-entry()
{
	echo "$TODAY ($NOW) - $1" >> $WATCHDOG_LOG
}

function crashplan-running()
{
	ps aux | grep "CrashPlan" | grep -q "java"
	echo $?
}

cp_status=$(crashplan-running)
if [ $cp_status -eq 0 ]; then
	echo $NOW > $WATCHDOG_FILE
else
	error=0
	if [ -e $WATCHDOG_FILE ]; then
		last=$(cat $WATCHDOG_FILE)
		delta=$((NOW-last))
		if [ $delta -gt $ERROR_BOUND ]; then
			error=1
			report-entry "crashplan exceeds watchdog bound ($NOW - $last = $delta > $ERROR_BOUND)"
		fi
	else
		error=1
		report-entry "no watchdog file"
	fi
	if [ $error -ne 0 ]; then
		report-entry "error reported by crashplan watchdog"
		systemctl start crashplan
		sleep 30
		cp_status=$(crashplan-running)
		report-entry "crashplan restarted, running check: $cp_status"
	fi
fi
```
