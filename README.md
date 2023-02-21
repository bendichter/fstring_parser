# fstring_parser

Use f-string syntax to parse values from strings.

fstring_parser allows you to *reverse* f-string syntax to extract data from strings. For example, let's say you had a 
bunch of strings like:

```python
strings = [
    "sub-001/sub-001a",
    "sub-001/sub-001b",
    "sub-002/sub-002a",
    "sub-002/sub-002b",
]
```

This library helps you extract the changing data from these strings. All you need to do is write an f-string syntax 
that would produce these strings, e.g.,:

```python
f"sub-{sub:03n}/sub-{sub:03n}{ses}"
```

You can now use this string to build a parser that will return the metadata of the string into those variables:

```python
from fstring_parser import parse_fstring

[parse_fstring("sub-{sub:03n}/sub-{sub:03n}{ses}", x) for x in strings]
```
```python
[{'sub': 1, 'ses': 'a'},
 {'sub': 1, 'ses': 'b'},
 {'sub': 2, 'ses': 'a'},
 {'sub': 2, 'ses': 'b'}]
```

The format options serve two purposes here. First, they serve to constrain the matches. Since the "sub" is formatted 
with the "n" data type, the library knows to only match characters that are digits. This much of the library can be 
reproduced using regex. Here is the equivalent regular expression for the above example.

```python
import re

pattern = re.compile('^sub\\-(?P<sub>0*-?[0-9]+)/sub\\-(?P=sub)(?P<ses>.+)$')
[pattern.match(x).groupdict() for x in strings]
```

Regular expressions can become quite difficult as the formatting gets more complex, and this library provides a much 
simpler syntax if you do not need more advanced matching. Second, this library infers the data type from the format 
and transforms the extracted data into the appropriate type. In this example, since "sub" was formatted with the "n" 
data type, it was transformed into an integer. You can disable this with the `transform=False`:

```python
[parse_fstring("sub-{sub:03n}/sub-{sub:03n}{ses}", x, transform=False) for x in strings]
```
```python
[{'sub': '001', 'ses': 'a'},
 {'sub': '001', 'ses': 'b'},
 {'sub': '002', 'ses': 'a'},
 {'sub': '002', 'ses': 'b'}]
```



## Installation

```
pip install fstring_parser
```
