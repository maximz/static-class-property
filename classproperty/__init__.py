"""Class Property."""

__author__ = """Maxim Zaslavsky"""
__email__ = "maxim@maximz.com"
__version__ = "0.0.1"


class classproperty(property):
    """
    A static readonly property on a class.
    From https://stackoverflow.com/a/7864317/130164
    Alternatives: https://stackoverflow.com/a/5191224/130164 and https://stackoverflow.com/a/5192374/130164

    Use this when you want to mark a method as @property and @staticmethod, or as @property and @classmethod. That doesn't work out of the box; you need this decorator instead.
    """

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()
