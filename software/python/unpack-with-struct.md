#### What does the 'format' of unpack mean?

Given this input:
```text
record = 'raymond   \x32\x12\x08\x01\x08'
```
and unpacking using this command

```text
unpack('<10sHHb', record)
```

The resulting tuple will have 4 entries that are basically this:

| Field | Value |
|-------|-------|
| name  | raymond |
| serial | 4658 |
| school | 264 |
| grade | 8 |

So how does 'raymond   \x32\x12\x08\x01\x08' + '<10sHHb' do it?

| Format Value | Description | Consumes | Value |
|--------------|-------------|----------|-------|
| <	| Little endian | | |
| 10s | 10 character string (10 bytes) | 'raymond   ' | 'raymond   ' |
| H | unsigned short (2 bytes) | \x32\x12 | 4658 (hex: 0x1232) |
| H | unsigned short (2 bytes) | \x08\x01 | 264 (hex: 0x108)  |
| b | signed char (1 byte) | \x08 | 8 |


#### Notes
* Pad (throw-away) using 'x' (e.g. <10s3xi) - throw away 3 bytes in the middle of a 10 char string and an int

#### References:

[1] https://docs.python.org/2/library/struct.html
