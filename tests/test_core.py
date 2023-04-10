from static_class_property import classproperty


class ClassWithStaticProperty:
    class_variable = "extra"

    @classproperty
    def static_property(cls):
        return f"static_property_{cls.class_variable}"


def test_classproperty():
    assert ClassWithStaticProperty.static_property == "static_property_extra"
    # reacts to class changes
    ClassWithStaticProperty.class_variable = "new"
    assert ClassWithStaticProperty.static_property == "static_property_new"
