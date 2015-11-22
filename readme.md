# my-object-id

A simple module for generate Mongodb ObjectID.

Tested on py2.7/py3.4

```python
from myobjectid import ObjectID

a = ObjectID()
b = ObjectID('56222d21293b328eb0000002')

a > b
>>> True

len(a)
>>>> 24

print(a)
>>>> 562237f4293b328a84000003

a.to_hex()
>>>> 562237f4293b328a84000003

a.to_bin()
>>>> 'V"7\xf4);2\x8a\x84\x00\x00\x03'

len(a.to_bin())
>>>> 12

```
