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
from . import models
from .doc_parsers import sphinx_doc_parser


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


def get_func_inspect_result(func, doc_parser=sphinx_doc_parser):
    """Get inspect results for a function

    :param function func: Function to inspect
    :return: Object with all the information related with the function
    :rtype: models.Function
    """
    arguments = []
    name = func.__name__
    args = get_function_args(func)
    default_args = get_default_args(func)
    short_description, long_description, doc_args, returns = doc_parser(func.__doc__)
    for position, arg in enumerate(args):
        doc_arg = doc_args.get(arg) or {}
        kind = doc_arg.get('type')
        description = doc_arg.get('doc')
        default = default_args.get(arg)
        is_arg = arg not in default_args  # if it doesn't have a default value, then it's an argument
        # name, default_value, kind, description, is_arg, position
        arguments.append(
            models.Argument(name=arg, default=default, kind=kind,
                            description=description, is_arg=is_arg, position=position)
        )
    return models.Function(name=name, short_description=short_description,
                           long_description=long_description, func=func,
                           arguments=arguments)
