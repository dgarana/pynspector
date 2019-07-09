# -* coding: utf-8 *-
"""
Set of tests for functions inspections module
"""
# System imports
import unittest

# Third-party imports
# Local imports
from .func_inspections import get_default_args, get_function_args, get_func_inspect_result
from . import models

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


class TestFunctionInspectResults(unittest.TestCase):
    """
    Test suite for function `get_func_inspect_result`
    """

    def test_should_parse_args_with_and_without_docstrings(self):
        def dummy_function(param_1, param_2):
            """Function to check something

            :param str param_1: Param one should be string
            """
            return

        func_res = get_func_inspect_result(dummy_function)
        self.assertIsInstance(func_res, models.Function)
        self.assertEqual(func_res.long_description, '')
        self.assertEqual(func_res.short_description, 'Function to check something')
        self.assertEqual(func_res.func, dummy_function)
        self.assertEqual(func_res.name, 'dummy_function')

        self._check_argument(
            func_res.arguments[0], name='param_1', description='Param one should be string',
            default=None, kind='str', is_arg=True, is_kwarg=False, position=0, mandatory=True
        )
        self._check_argument(
            func_res.arguments[1], name='param_2', description=None,
            default=None, kind=None, is_arg=True, is_kwarg=False, position=1, mandatory=True
        )

    def test_should_parse_kwargs_with_and_without_docstrings(self):
        def dummy_function(param_1='Hello', param_2=None):
            """Function to check something

            :param str param_1: Param one should be string
            """
            return

        func_res = get_func_inspect_result(dummy_function)
        self.assertEqual(func_res.name, 'dummy_function')
        self._check_argument(
            func_res.arguments[0], name='param_1', description='Param one should be string',
            default='Hello', kind='str', is_arg=False, is_kwarg=True, position=0, mandatory=False
        )
        self._check_argument(
            func_res.arguments[1], name='param_2', description=None,
            default=None, kind=None, is_arg=False, is_kwarg=True, position=1, mandatory=False
        )

    def _check_argument(self, argument, name, description, kind, default, is_arg, is_kwarg, position, mandatory):
        self.assertIsInstance(argument, models.Argument)
        self.assertEqual(argument.name, name)
        self.assertEqual(argument.description, description)
        self.assertEqual(argument.kind, kind)
        self.assertEqual(argument.default, default)
        self.assertEqual(argument.is_arg, is_arg)
        self.assertEqual(argument.is_kwarg, is_kwarg)
        self.assertEqual(argument.position, position)
        self.assertEqual(argument.is_mandatory, mandatory)


if __name__ == '__main__':
    unittest.main()
