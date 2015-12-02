#### 

```text
record = 'raymond   \x32\x12\x08\x01\x08'
unpack('<10sHHb', record)
```
* Which becomes
| Field | Value |
|-------|-------|
| name  | raymond |
| serial | 4658 |
| school | 264 |
| grade | 8 |

#### References:

[1] https://docs.python.org/2/library/struct.html
