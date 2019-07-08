# -* coding: utf-8 *-
"""
Set of tests for functions inspections module
"""
# System imports
import unittest

# Third-party imports
# Local imports
from .func_inspections import get_default_args, get_function_args


# ####################
#  Example functions #
# ####################

def func_with_no_arguments():
    pass


def func_with_no_defaults(foo, bar):
    return foo, bar


def func_with_some_defaults(foo, bar=1):
    return foo, bar


class TestGetDefaultArgs(unittest.TestCase):
    """
    Test suite for function `get_default_args`
    """

    def test_should_return_nothing_when_no_defaults(self):
        default_args = get_default_args(func_with_no_defaults)
        self.assertDictEqual(default_args, {})

    def test_should_return_only_arguments_with_defaults(self):
        default_args = get_default_args(func_with_some_defaults)
        self.assertDictEqual(default_args, {'bar': 1})

    def test_should_work_with_no_arguments(self):
        default_args = get_default_args(func_with_no_arguments)
        self.assertDictEqual(default_args, {})


class TestFunctionArgs(unittest.TestCase):
    """
    Test suite for function `get_function_args`
    """

    def test_return_all_arguments_from_function(self):
        arguments = get_function_args(func_with_no_defaults)
        self.assertListEqual(arguments, ['foo', 'bar'])

    def test_return_all_arguments_from_function_even_defaults(self):
        arguments = get_function_args(func_with_no_defaults)
        self.assertListEqual(arguments, ['foo', 'bar'])

    def test_return_empty_when_no_arguments(self):
        arguments = get_function_args(func_with_no_arguments)
        self.assertListEqual(arguments, [])


if __name__ == '__main__':
    unittest.main()
