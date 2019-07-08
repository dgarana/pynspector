# -* coding: utf-8 *-
"""
:py:mod:`pynspector.module_inspections`
---------------------------------------
Main module for inspecting modules
"""
# System imports
from inspect import isfunction, getmembers

# Third-party imports
# Local imports


__all__ = ['get_module_functions']


def get_module_functions(module):
    """Get functions for a given module

    Return all public functions that are available on a module.

    Example:
    >>> from pynspector import module_inspections_fixture_test
    >>> functions = get_module_functions(module_inspections_fixture_test)
    >>> list(functions)
    >>> [module_inspections_fixture_test.dummy_func]
    >>> type(functions)
    >>> <type 'generator'>

    :param module module: Module to inspect for functions
    :return: Generator that returns functions that are available under this module
    :rtype: generator
    """

    return (
        func for name, func in getmembers(module)
        if not name.startswith("_") and isfunction(func)
    )
