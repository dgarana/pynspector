# -* coding: utf-8 *-
"""
:py:mod:`pynspector.doc_parser`
-------------------------------
Here you will find parsers for docstrings, this will help you to retrieve all
arguments, types and descriptions defined on docstrings.

You can use different parsers such as:
- sphinx_doc_parser
"""
# System imports
import re
import sys

# Third-party imports
# Local imports


__all__ = ['sphinx_doc_parser']


PARAM_OR_RETURNS_REGEX = re.compile(r":(?:param|returns|return)")
RETURNS_REGEX = re.compile(
    r":(returns|return): (?P<doc>.*)(?:(?=:param)|(?=:raises)|(?=:rtype)|(?=:type)|\Z)", re.S
)
TYPE_REGEX = re.compile(
    r":type (?P<name>[\*\w]+): (?P<type>.*?)(?:(?=:param)|"
    r"(?=:return)|(?=:returns)|(?=:raises)|(?=:rtype)|\Z)", re.S
)
PARAM_REGEX = re.compile(
    r":param (?P<type>.*?)(?P<name>[\*\w]+): (?P<doc>.*?)(?:(?=:param)|"
    r"(?=:return)|(?=:returns)|(?=:raises)|(?=:rtype)|(?=:type)|\Z)", re.S
)


def _trim(docstring):
    """trim function from PEP-257

    :param str docstring: Docstring in string format
    :return: Docstring parsed with trim.
    :rtype: str
    """
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    # Current code/unittests expects a line return at
    # end of multiline docstrings
    # workaround expected behavior from unittests
    if "\n" in docstring:
        trimmed.append("")

    # Return a single string:
    return "\n".join(trimmed)


def _reindent(string):
    """Reindent string"""
    return "\n".join(l.strip() for l in string.strip().split("\n"))


def sphinx_doc_parser(docstring):
    """Parse docstring and return short, long and arguments for this function
    
    This parser should work as sphinx does by default. It should be able to parse
    docstrings following next format:

    ```
    Title of the docstring

    Long description goes here, with
    multiline support.

    :param str argument_one: Argument one description
    :param argument_two: Argument two description
    :type argument_two: str
    :return: What the function returns
    ```

    - The short description or title is mandatory (at least for now).
    - The long description is optional, it will report "" if there's no long description available.
    - The param type is not mandatory, if there's no type for a param, it will report it as None.
    - The return statement could be also "returns", both works fine.

    :param str docstring: Docstring in string format
    :returns: Tuple with short_description, long_description, params, returns
    :rtype: tuple
    """
    short_description = long_description = returns = ""
    params = {}

    if docstring:
        docstring = _trim(docstring)

        lines = docstring.split("\n", 1)
        short_description = lines[0]

        if len(lines) > 1:
            long_description = lines[1].strip()

            params_returns_desc = None

            match = PARAM_OR_RETURNS_REGEX.search(long_description)
            if match:
                long_desc_end = match.start()
                params_returns_desc = long_description[long_desc_end:].strip()
                long_description = long_description[:long_desc_end].rstrip()

            if params_returns_desc:
                params = {}
                for type_, name, doc in PARAM_REGEX.findall(params_returns_desc):
                    params[name] = {'doc': ' '.join(_trim(doc).split('\n')),
                                    'type': type_.strip() if type_ else None}

                match = RETURNS_REGEX.search(params_returns_desc)
                if match:
                    returns = _reindent(match.group("doc"))

                for name, type_ in TYPE_REGEX.findall(params_returns_desc):
                    type_ = type_.strip()
                    if name in params:
                        params[name].update({'type': type_})
                    else:
                        params[name] = {'doc':'', 'type': type_}

    return short_description, long_description, params, returns
