from typing import NamedTuple

class Sensors(NamedTuple):
    name: str
    data: float
    timestamp: int
    min_threshold: list
    max_threshold: float

my_item = Sensors('foo', 0,0, ['baz'],0)
print(my_item.name)

print(int(float('1.234')))

print(my_item) # MyStruct(foo='foo', bar=0, baz=['baz'], qux=User(name='peter'))