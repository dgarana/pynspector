# -* coding: utf-8 *-
"""
Set of tests for testing doc_parsers module
"""
# System imports
import unittest

# Third-party imports
# Local imports
from pynspector.doc_parsers import sphinx_doc_parser


class TestSphinxDocParser(unittest.TestCase):
    def test_it_should_return_params_without_type(self):
        docstring = """
            Title

            :param name: Here goes the name
            """
        _, _, params, _ = sphinx_doc_parser(docstring)
        self.assertIn('name', params)
        self.assertIsNone(params['name']['type'])

    def test_it_should_return_params_with_type(self):
        docstring = """
            Title

            :param str name: Here goes the name
        """
        _, _, params, _ = sphinx_doc_parser(docstring)
        self.assertIn('name', params)
        self.assertEqual('str', params['name']['type'])

    def test_should_accept_returns_statement(self):
        docstring = """
            Title
            
            :returns: Here goes the returns
        """
        _, _, _, returns = sphinx_doc_parser(docstring)
        self.assertEqual('Here goes the returns', returns)

    def test_should_accept_return_statement(self):
        docstring = """
            Title
            
            :return: Here goes the return
        """
        _, _, _, returns = sphinx_doc_parser(docstring)
        self.assertEqual('Here goes the return', returns)

    def test_should_not_fail_when_no_docstring(self):
        docstring = None
        self.assertEqual(
            ("", "", {}, ""),
            sphinx_doc_parser(docstring)
        )

    def test_should_accept_type_statement(self):
        docstring = """
            Title
            
            :param foo: Description goes here
            :type foo: bool
        """
        _, _, param, _ = sphinx_doc_parser(docstring)
        self.assertIn('foo', param)
        self.assertEqual('bool', param['foo']['type'])

    def test_param_and_type_works_together(self):
        docstring = """
            Title
            
            Subtitle
            
            :param foo: Description foo goes here
            :type foo: bool
            :param str bar: Description bar goes here
        """
        _, _, params, _ = sphinx_doc_parser(docstring)
        self.assertIn('foo', params)
        self.assertEqual('bool', params['foo']['type'])
        self.assertIn('bar', params)
        self.assertEqual('str', params['bar']['type'])

    def test_multiline_subtitle(self):
        docstring = """
            Title
            
            Subtitle could be
            multiline.
        """
        _, long_, _, _ = sphinx_doc_parser(docstring)
        self.assertEqual('Subtitle could be\nmultiline.', long_)


if __name__ == '__main__':
    unittest.main()
