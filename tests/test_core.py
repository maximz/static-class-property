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
    assert (
        ClassWithStaticProperty().static_property == "static_property_new2"
    )  # new instance

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
    assert (
        ClassWithStaticPropertyAndMetaclass.static_property == "static_property_extra"
    )
    instance = ClassWithStaticPropertyAndMetaclass()

    # Can't set on class
    with pytest.raises(ValueError, match="Cannot set static_property"):
        ClassWithStaticPropertyAndMetaclass.static_property = "different"
    assert instance.static_property == "static_property_extra"
    assert (
        ClassWithStaticPropertyAndMetaclass.static_property == "static_property_extra"
    )

    # Can't set on instance
    instance = ClassWithStaticPropertyAndMetaclass()
    assert instance.static_property == "static_property_extra"
    with pytest.raises(AttributeError, match="can't set attribute 'static_property'"):
        instance.static_property = "different2"
    assert instance.static_property == "static_property_extra"
    assert (
        ClassWithStaticPropertyAndMetaclass.static_property == "static_property_extra"
    )

    # other properties work as expected
    assert ClassWithStaticPropertyAndMetaclass.class_variable == "extra"
    ClassWithStaticPropertyAndMetaclass.class_variable = "extranew"
    assert ClassWithStaticPropertyAndMetaclass.class_variable == "extranew"
    assert (
        instance.class_variable == "extranew"
    )  # pre-existing instance sees the change
    assert (
        ClassWithStaticPropertyAndMetaclass().class_variable == "extranew"
    )  # new instance sees the change too

    # All the usual tests:

    # reacts to class changes
    assert (
        ClassWithStaticPropertyAndMetaclass.static_property
        == "static_property_extranew"
    )
    assert (
        instance.static_property == "static_property_extranew"
    )  # pre-existing instance
    assert (
        ClassWithStaticPropertyAndMetaclass().static_property
        == "static_property_extranew"
    )  # new instance

    # no reaction to instance changes, still points to class-level value:
    instance.class_variable = "totally new"
    assert ClassWithStaticPropertyAndMetaclass.class_variable == "extranew"
    assert instance.static_property == "static_property_extranew"
    assert (
        ClassWithStaticPropertyAndMetaclass.static_property
        == "static_property_extranew"
    )
    assert (
        ClassWithStaticPropertyAndMetaclass().static_property
        == "static_property_extranew"
    )  # new instance


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
    class_variable = "extra2"

    @classproperty
    def static_property_overloaded(cls):
        return f"static_property_overloaded2_{cls.class_variable}"


def test_inheritance():
    # Test inheritance:
    # does it work if not overloaded: yes, and cls points to child class as expected
    assert (
        BaseClass.static_property_not_overloaded
        == BaseClass().static_property_not_overloaded
        == "static_property_not_overloaded_extra"
    )
    assert (
        ChildClass.static_property_not_overloaded
        == ChildClass().static_property_not_overloaded
        == "static_property_not_overloaded_extra2"
    )

    # and can you still overload: yes
    assert (
        BaseClass.static_property_overloaded
        == BaseClass().static_property_overloaded
        == "static_property_overloaded_extra"
    )
    assert (
        ChildClass.static_property_overloaded
        == ChildClass().static_property_overloaded
        == "static_property_overloaded2_extra2"
    )

    # Can't set on class
    # TODO: This one is broken:
    # with pytest.raises(ValueError, match="Cannot set static_property_not_overloaded"):
    #     ChildClass.static_property_not_overloaded = "different"
    with pytest.raises(ValueError, match="Cannot set static_property_overloaded"):
        BaseClass.static_property_overloaded = "different"
    with pytest.raises(ValueError, match="Cannot set static_property_overloaded"):
        ChildClass.static_property_overloaded = "different"

    # Can't set on instance
    with pytest.raises(AttributeError, match="can't set attribute"):
        ChildClass().static_property_not_overloaded = "different"
    with pytest.raises(AttributeError, match="can't set attribute"):
        BaseClass().static_property_overloaded = "different"
    with pytest.raises(AttributeError, match="can't set attribute"):
        ChildClass().static_property_overloaded = "different"


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


# TODO: Change all classvar to this pattern, including with abstract property.
# And mention in our docs here that this is where it should be used.


def test_abstract():
    # Test for abstract base class: can we keep it abstract property? Yes
    with pytest.raises(NotImplementedError):
        AbstractBaseClass.static_property
    with pytest.raises(NotImplementedError):
        AbstractBaseClass().static_property

    assert ConcreteClass.static_property == "static_property_overloaded_extra2"
    assert ConcreteClass().static_property == "static_property_overloaded_extra2"

    # Can't set on class
    with pytest.raises(ValueError, match="Cannot set static_property"):
        AbstractBaseClass.static_property = "different"
    with pytest.raises(ValueError, match="Cannot set static_property"):
        ConcreteClass.static_property = "different"

    # Can't set on instance
    with pytest.raises(AttributeError, match="can't set attribute"):
        AbstractBaseClass().static_property = "different"
    with pytest.raises(AttributeError, match="can't set attribute"):
        ConcreteClass().static_property = "different"
