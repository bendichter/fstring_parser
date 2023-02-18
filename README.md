# fstring_parser

This library uses f-string syntax to parse a string and values.

## Example

```python```
# create string
x = 5555555
string = f"abc{x:,}abc123"
print(string)
```
```
abc5,555,555abc123
```

```python
# recover data from string
from fstring_parser import parse_fstring
parse_fstring("abc{x:,}abc123", "abc5,555,555abc123")
```
```
{'x': 5555555}
```


## Installation

pip install fstring_parser