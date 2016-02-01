Large Cursor
============

In some cases a GTK application will pull in Adwaita and that can cause a 'comically large' mouse cursor

```
vim /usr/share/icons/default/index.theme
---
#Comment out this line
Inherits=Adwaita
```
