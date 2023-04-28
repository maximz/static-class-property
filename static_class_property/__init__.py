"""Class Property."""

__author__ = """Maxim Zaslavsky"""
__email__ = "maxim@maximz.com"
__version__ = "0.0.2"
from typing import Any


class GetOnlyProperty(object):
    """Like standard property, but always read-only: doesn't allow set or delete."""

    # Based on https://docs.python.org/3/howto/descriptor.html#properties
    def __init__(self, fget=None, doc=None):
        self.fget = fget
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc
        self._name = ""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError(f"property '{self._name}' has no getter")
        return self.fget(obj)

    def getter(self, fget):
        prop = type(self)(fget=fget, doc=self.__doc__)
        prop._name = self._name
        return prop

    def __set__(self, obj, value):
        # Prevents set on class *instance*. (Doesn't prevent set on the class itself - that's handled separately)
        raise AttributeError(f"can't set attribute '{self._name}'")

    def __delete__(self, obj):
        # TODO: test whether this prevents delete on a class instance.
        raise AttributeError(f"can't delete attribute '{self._name}'")


class classproperty(GetOnlyProperty):
    """
    A static, readonly property on a class.
    From https://stackoverflow.com/a/7864317/130164
    Alternatives: https://stackoverflow.com/a/5191224/130164 and https://stackoverflow.com/a/5192374/130164

    Use this when you want to mark a method as @property and @staticmethod, or as @property and @classmethod. That doesn't work out of the box; you need this decorator instead.

    Make sure to use the metaclass to make the property read-only on the class itself, not just on instances.
    Without the metaclass, setting Class.property = "test" will work, but setting Class().property = "test" will not.
    This is because Class.property just changes the binding.
    """

    def __get__(self, instance: None, instance_type: Any) -> Any:
        # todo: can we simplify the fget in the property? test to make sure it works w/ and w/o classmethod decorator too?
        # return self.fget.__get__(None, objtype)()
        # return self.fget(instance_type) # this works unless also wrapped in @classmethod

        # Wrap the fget in a classmethod, then call it with the class as the cls
        wrapped_property_getter = classmethod(self.fget)
        return wrapped_property_getter.__get__(
            instance, instance_type
        )()  # TODO: instance, or None?


class MetaClassContainingClassProperties(type):
    def __new__(meta, name, bases, attrs):
        # TODO: Run monkeytype and get types for this.
        # Find which attrs are classproperties
        attrs_that_should_not_be_edited_after_definition = {
            attrname
            for attrname, attrval in attrs.items()
            if isinstance(attrval, classproperty)
        }
        # handle inherited classproperties from base classes that are not overloaded in child class
        for parent_class in bases:
            # set union
            attrs_that_should_not_be_edited_after_definition |= {
                baseclass_attrname
                for baseclass_attrname, baseclass_attrval in parent_class.__dict__.items()
                if isinstance(baseclass_attrval, classproperty)
                # don't add if we already examined above (i.e. skip if overloaded or unique to child class)
                and baseclass_attrname not in attrs.keys()
            }

        new_instance = super().__new__(meta, name, bases, attrs)

        # Store names of anything in attrs that isinstance classproperty
        new_instance._cantchange = attrs_that_should_not_be_edited_after_definition

        return new_instance

    def __setattr__(cls, attr, value):
        # Overload as in https://stackoverflow.com/a/42360496/130164
        # Prevents setting the property on the class itself (doesn't prevent set on a class instance - that's handled separately)

        # Skip this check when the initial set of _cantchange is performed by __new__()
        if attr != "_cantchange":

            if hasattr(cls, "_cantchange"):  # Skip this check if chaining metaclasses

                if attr in cls._cantchange:
                    # Reject setting the property on the class itself
                    raise ValueError(f"Cannot set {attr}")

        # Process the change
        return super().__setattr__(attr, value)
