# pylint: disable=missing-module-docstring,missing-function-docstring,too-many-lines,consider-using-f-string
import textwrap

import pytest
from saltrewrite.salt import fix_docstrings


def test_fix_codeblock(tempfiles):
    code = textwrap.dedent(
        """
    def one():
        '''
        One was a function like:

        ..code-block::python
            one()

        '''
        print("one")
    """
    )
    expected_code = textwrap.dedent(
        """
    def one():
        '''
        One was a function like:

        .. code-block:: python

            one()

        '''
        print("one")
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_docstrings.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_fix_codeblock_with_config(tempfiles):
    code = textwrap.dedent(
        """
    def one():
        '''
        One was a function like:

        ..code-block::python
            :linenos:
            one()

        '''
        print("one")
    """
    )
    expected_code = textwrap.dedent(
        """
    def one():
        '''
        One was a function like:

        .. code-block:: python
            :linenos:

            one()

        '''
        print("one")
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_docstrings.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_cli_example(tempfiles):
    code = textwrap.dedent(
        """
    def one():
        '''
        One was a function like:
        Cli ExamplE:

            salt one

        '''
        print("one")
    """
    )
    expected_code = textwrap.dedent(
        """
    def one():
        '''
        One was a function like:

        CLI Example:

        .. code-block:: bash

            salt one

        '''
        print("one")
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_docstrings.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


@pytest.mark.parametrize("vtype", ["versionadded", "versionchanged", "deprecated"])
def test_fix_versionadded(tempfiles, vtype):
    code = textwrap.dedent(
        """
    def one():
        '''
        One was a function like:

        ..{}: Neon

        Returns {{deprecated: true}} if the thing type was deprecated and returns
        {{deprecated: false}} if the thing type was not deprecated.
        '''
        print("one")
    """.format(
            vtype
        )
    )
    expected_code = textwrap.dedent(
        """
    def one():
        '''
        One was a function like:

        .. {}:: 3000

        Returns {{deprecated: true}} if the thing type was deprecated and returns
        {{deprecated: false}} if the thing type was not deprecated.
        '''
        print("one")
    """.format(
            vtype
        )
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_docstrings.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


@pytest.mark.parametrize("vtype", ["versionadded", "versionchanged", "deprecated"])
def test_fix_versionadded_multiple(tempfiles, vtype):
    code = textwrap.dedent(
        """
    def one():
        '''
        One was a function like:

        ..{}:Neon,3001
        '''
        print("one")
    """.format(
            vtype
        )
    )
    expected_code = textwrap.dedent(
        """
    def one():
        '''
        One was a function like:

        .. {}:: 3000,3001
        '''
        print("one")
    """.format(
            vtype
        )
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_docstrings.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


@pytest.mark.parametrize("vtype", ["versionadded", "versionchanged", "deprecated"])
def test_fix_versionadded_module_docstring(tempfiles, vtype):
    code = textwrap.dedent(
        """
    # -*- coding: utf-8 -*-
    '''
    New module blah

    ..{}:Neon,3001
    '''

    def one():
        '''
        One function
        '''
        print("one")
    """.format(
            vtype
        )
    )
    expected_code = textwrap.dedent(
        """
    # -*- coding: utf-8 -*-
    '''
    New module blah

    .. {}:: 3000,3001
    '''

    def one():
        '''
        One function
        '''
        print("one")
    """.format(
            vtype
        )
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_docstrings.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_global_scoped_variables_with_docstring(tempfiles):
    code = textwrap.dedent(
        """
    '''
    Blah Module docstring
    '''

    HAS_LIB = False
    try:
        import it
    except ImportError:
        HAS_LIB = False

    def one():
        '''
        One was a function like:

        ..code-block::python
            one()

        '''
        print("one")
    """
    )
    expected_code = textwrap.dedent(
        """
    '''
    Blah Module docstring
    '''

    HAS_LIB = False
    try:
        import it
    except ImportError:
        HAS_LIB = False

    def one():
        '''
        One was a function like:

        .. code-block:: python

            one()

        '''
        print("one")
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_docstrings.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_global_scoped_variables_without_docstring(tempfiles):
    code = textwrap.dedent(
        """
    HAS_LIB = False
    try:
        import it
    except ImportError:
        HAS_LIB = False

    def one():
        '''
        One was a function like:

        ..code-block::python
            one()

        '''
        print("one")
    """
    )
    expected_code = textwrap.dedent(
        """
    HAS_LIB = False
    try:
        import it
    except ImportError:
        HAS_LIB = False

    def one():
        '''
        One was a function like:

        .. code-block:: python

            one()

        '''
        print("one")
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_docstrings.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
