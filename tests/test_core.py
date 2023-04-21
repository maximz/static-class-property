import pytest
from static_class_property import MetaClassContainingClassProperties, classproperty


class ClassWithStaticProperty:
    # normal attribute
    class_variable = "extra"

    # our special static property
    @classproperty
    def static_property(cls):
        return f"static_property_{cls.class_variable}"


def test_classproperty():
    assert ClassWithStaticProperty.static_property == "static_property_extra"

    # reacts to class changes
    ClassWithStaticProperty.class_variable = "new"
    assert ClassWithStaticProperty.static_property == "static_property_new"

    # works in an instance
    instance = ClassWithStaticProperty()
    assert instance.static_property == "static_property_new"

    # instance reacts to class changes (even if instance was created before the change)
    ClassWithStaticProperty.class_variable = "new2"
    assert ClassWithStaticProperty.static_property == "static_property_new2"
    assert instance.class_variable == "new2"
    assert instance.static_property == "static_property_new2"

    # but no reaction to instance changes! still points to class-level value.
    instance.class_variable = "new3"
    assert ClassWithStaticProperty.class_variable == "new2"
    assert instance.static_property == "static_property_new2"
    assert ClassWithStaticProperty.static_property == "static_property_new2"

    # Can't set on instance
    with pytest.raises(AttributeError, match="can't set attribute"):
        instance.static_property = "replaced"
    assert instance.static_property == "static_property_new2"
    assert ClassWithStaticProperty.static_property == "static_property_new2"

    # But can set on class (and it changes for all instances), since we are not using the metaclass
    ClassWithStaticProperty.static_property = "replaced"
    assert ClassWithStaticProperty.static_property == "replaced"
    assert instance.static_property == "replaced"


####


class ClassWithStaticPropertyAndMetaclass(metaclass=MetaClassContainingClassProperties):
    class_variable = "extra"

    @classproperty
    def static_property(cls):
        return f"static_property_{cls.class_variable}"


def test_classproperty_readonly():
    pass
    Foo.backend  # "mybackend"
    # Can't change before initialization
    Foo.backend = "test"  # ValueError: cannot set backend

    # Can't change after initialization
    f = Foo()
    f.backend  # "mybackend"
    f.backend = "test"  # AttributeError: can't set attribute 'backend'

    # other properties work as expected
    Foo.normal  # 5
    Foo.normal = 6
    Foo.normal  # 6
    f.normal  # dunno
    Foo().normal  # 6


####


class BaseClass(metaclass=MetaClassContainingClassProperties):
    class_variable = "extra"

    @classproperty
    def static_property_not_overloaded(cls):
        return f"static_property_not_overloaded_{cls.class_variable}"

    @classproperty
    def static_property_overloaded(cls):
        return f"static_property_overloaded_{cls.class_variable}"


class ChildClass(BaseClass):
    @classproperty
    def static_property_overloaded(cls):
        return f"static_property_overloaded2_{cls.class_variable}"


def test_inheritance():
    # TODO
    # Test inheritance. does it work if not overloaded. and can you still overload
    pass


####

from abc import ABCMeta, abstractmethod


def combine_classes(*args):
    # https://stackoverflow.com/a/62849795/130164
    name = "".join(a.__name__ for a in args)
    return type(name, args, {})


class AbstractBaseClass(
    metaclass=combine_classes(MetaClassContainingClassProperties, ABCMeta)
):
    class_variable = "extra"

    @classproperty
    @abstractmethod
    def static_property(cls):
        raise NotImplementedError()


class ConcreteClass(AbstractBaseClass):
    class_variable = "extra2"

    @classproperty
    def static_property(cls):
        return f"static_property_overloaded_{cls.class_variable}"


# TODO: Change all classvar to this pattern. And mention in our docs here that this is where it should be used
def test_abstract():
    # TODO
    # but for abstract base class, can we keep it abstract property somehow. add that as a test too
    pass
