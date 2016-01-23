Start/Auto Login (debian)
=========================

Make sure x is install (mainly startx) and the preferred WM
```
sudo apt-get install xorg <wm>
```

Update X11 to support anybody to 'start x', edit /etc/X11/Xwrapper.config
```
allowed_users=anybody
```

Create a file /etc/systemd/system/xinit-login.service
```
[Unit]
After=systemd-user-sessions.service

[Service]
ExecStart=/bin/su <username> -l -c /usr/bin/startx

[Install]
WantedBy=multi-user.target
```

Enable via systemd
```
systemctl daemon-reload
systemctl enable xinit-login.service
systemctl start xinit-login.service
```

## References
[1] https://wiki.gentoo.org/wiki/X_without_Display_Manager
[2] http://karuppuswamy.com/wordpress/2010/09/26/how-to-fix-x-user-not-authorized-to-run-the-x-server-aborting/
