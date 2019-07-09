# -* coding: utf-8 *-
"""
:py:mod:`pynspector.models`
---------------------------
Here you will find all models that are used across pynspector.

What is a model?
================
A model is just a class that holds some attributes and is returned as a result of an operation.
"""
# System imports
import inspect

# Third-party imports
# Local imports


class Argument(object):
    """Argument object

    This object represents an argument that is passed to a function.
    Whenever you inspect a function, you will get a function object with all it's arguments in this format.
    """

    def __init__(self, name, default, kind, description, is_arg, position):
        """ Initialize Argument object

        :param str name: Name of the argument
        :param default: Default value for this argument
        :param str kind: The type of this argument
        :param str description: Description for this argument
        :param bool is_arg: Returns if the argument is arg or kwarg (keyword argument)
        :param int position: Position in arg list
        """
        self.name = name
        self.default = default
        self.kind = kind
        self.description = description
        self.is_arg = is_arg
        self.position = position

    @property
    def is_kwarg(self):
        return not self.is_arg

    @property
    def is_mandatory(self):
        """Returns if the argument is mandatory or not"""
        return self.is_arg


class Function(object):
    """Function object

    This object represents a function
    """

    def __init__(self, name, short_description, long_description, func, arguments):
        self.name = name
        self.short_description = short_description
        self.long_description = long_description
        self.func = func
        self.source_code = inspect.getsource(func)
        self.arguments = arguments or []
