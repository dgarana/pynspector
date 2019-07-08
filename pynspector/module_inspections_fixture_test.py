# -* coding: utf-8 *-
"""
Fixture module for module inspections test
"""
# System imports
# Third-party imports
# Local imports


AN_ATTRIBUTE = "This should not be returned"
_ANOTHER_ATTRIBUTE = "Neither this one"


def _dummy_func():
    """This should not be returned"""
    pass


def dummy_func():
    """This should be returned"""
    pass


class JustAClass(object):
    """This class should not be returned"""
    pass
