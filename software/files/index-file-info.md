Encrypt/Decrypt File Info
=========================

Generate a tree structure (for reference) at the root of the mount
```
tree .
```

Generate hashsums for all files in a mounted image
```
find -type f -exec sha512sum "{}" +
```

Archiving in images
```
tar czf <name>.tar.gz <dir>/*
```
