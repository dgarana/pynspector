# -* coding: utf-8 *-
"""
:py:mod:`pynspector.func_inspections`
-------------------------------------
Main module for inspecting functions
"""
# System imports
import inspect

# Third-party imports
# Local imports


__all__ = ['get_function_args', 'get_default_args']


def get_default_args(func):
    """ Get default arguments for a function

    Return default arguments for a given function, if function has no default arguments, it
    returns an empty dictionary.

    Example:
    >>> def func(foo, bar=None):
    ...     pass
    >>> get_default_args(func)
    >>> {'bar': None}

    :param function func: Function to get default arguments
    :return: Dictionary with argument as key and default value as value
    :rtype: dict
    """
    args, varargs, keywords, defaults = inspect.getargspec(func)
    if not defaults:
        return {}
    return dict(zip(args[-len(defaults):], defaults))


def get_function_args(func):
    """ Get all the arguments defined on a function

    Example:
    >>> def example_func(foo, bar=None):
    >>>    return foo, bar
    >>> get_function_args(example_func)
    >>> ['foo', 'bar']

    :param func func: Function to inspect
    :return: List of arguments
    :rtype: list
    """
    arg_spec = inspect.getargspec(func)
    return arg_spec.args
