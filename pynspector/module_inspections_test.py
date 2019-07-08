# -* coding: utf-8 *-
"""
Set of tests for testing module inspections
"""
# System imports
import unittest

# Third-party imports
# Local imports
from pynspector.module_inspections import get_module_functions
from pynspector import module_inspections_fixture_test


def dummy_func():
    return


def _dummy_func():
    return


class DummyObject(object):
    pass


class TestGetModuleFunctions(unittest.TestCase):
    """
    Test suite for function `get_module_functions`
    """
    def test_it_should_get_only_functions(self):
        self.assertListEqual(
            [module_inspections_fixture_test.dummy_func],
            list(get_module_functions(module_inspections_fixture_test))
        )


if __name__ == '__main__':
    unittest.main()
