
<h1 align="center">ihoop</h1>
<h2 align="center">Strict, immutable Abstract/Final classes</h2>

Do you like python, but wish it is was more like Julia? Do like Julia, but wish it was a language other people used? Did you read *Design Patterns: Elements of Reusable Object-Oriented Software*, but wish you didn't? 

Meet `ihoop`: a tiny library that turns plain Python classes into frozen, Abstract/Final instances. Drop in `Strict` as a base class and get:
- Immutability by default: once `__init__` finishes, your objects are read-only.  
- Abstract or Final:
  - Abstract classes: can be subclassed, but cannot be instantiated.  
  - Concrete classes: can be instantiated, but cannot be subclassed.  
-Abstract attributes, not just methods: Declare with `AbstractAttribute[T]`; subclasses must supply (via type hints) a real value.
- No dependencies: pure Python.


This package was largely ~~copied~~ inspired by [equinox](https://docs.kidger.site/equinox/)'s `strict=True` flag. For more information see https://docs.kidger.site/equinox/pattern/.

Why is it called `ihoop`? Because (i) (h)ate (o)bject (o)riented (p)rogramming 😉

## Example

```python
from ihoop import Strict, AbstractAttribute

class AbstractAnimal(Strict):
    name: AbstractAttribute[str]

class Dog(AbstractAnimal):
    name: str

    def __init__(self, name: str):
        self.name = name

>>> Dog("Fido").name
'Fido'
>>> d = Dog("Rex")
>>> d.name = "Max"
AttributeError: Cannot set attribute 'name' on frozen instance of Dog. strict objects are immutable after initialization.
```

## Sharp Edges

- It is important to type hint all member variables at the class level. It is very possible to bypass the checking/enforcement of `Strict` by doing things in the `__init__`.

## Roadmap

- [x] dataclass testing and integration
- [ ] abstractclassvar: strictness for class variables
- [ ] Package for pypi
