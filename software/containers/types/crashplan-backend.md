CrashPlan (backend) PRO
=======================

Before starting make sure to download the latest CrashPlan (PRO) archive, this will be a headless setup

Install the necessary packages
```
pacman -S cpio 
```

Move into the working area and unpack the CrashPlan archive
```
cd /opt
mv CrashPlanPro<version>.tgz .
tar xzvf CrashPlanPro<version>.tgz
```

Run the CrashPlan install, at the prompts use these settings
```
# Parent directory
/opt

# CrashPlan executable
/usr/local/bin

# Incoming data
/opt/crashplan/manifest

# SYSV init
/etc/init.d

# runlevel
/etc/rc5.d
```

Setup logging (for host access)
```
rm -rf /opt/crashplan/log

# For 'export' to the host machine for it to access/monitor
ln -s /opt/containers/logs/cp /opt/crashplan/log
```

Install [watchdog](https://github.com/enckse/howdoi/blob/master/software/crashplan/crashplan-watchdog.md) to '/opt/crashplan-watcher' and enable in crontab
