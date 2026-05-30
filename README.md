# static_class_property

`static_class_property` provides a tiny `@classproperty` decorator for
Python classes. It lets a method be read like a property on the class while the
getter still receives the class object, making it useful for values computed
from other class attributes.

## Why it exists

Python's built-in `@property` is for instance attributes. Stacking `@property`
with `@staticmethod` or `@classmethod` does not create a class-level property,
so this package supplies the descriptor needed for that pattern.

## Installation

```bash
pip install static_class_property
```

The package declares support for Python 3.8 and newer and has no runtime
dependencies.

## Usage

```python
from static_class_property import classproperty


class Settings:
    env = "prod"

    @classproperty
    def label(cls):
        return f"settings:{cls.env}"


assert Settings.label == "settings:prod"

Settings.env = "dev"
assert Settings.label == "settings:dev"
```

Use the getter argument like `cls` in a `@classmethod`: it is bound to the owner
class each time the attribute is read.

## How it works

`classproperty` subclasses `property` and implements `__get__`. On access, it
wraps the original getter with `classmethod`, binds it to the owner class, and
calls it immediately.

## Behavior and limitations

- The value is recomputed on every access; there is no caching.
- The decorator is intended for read-only computed class values.
- Assigning to the attribute on the class replaces the descriptor, as with any
  normal class attribute.

## Development

```bash
pip install -r requirements_dev.txt
pip install -e .
make test
make lint
```

Docs can be built with `make docs`.

## License

MIT License.
