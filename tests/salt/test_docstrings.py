# pylint: disable=missing-module-docstring,missing-function-docstring,too-many-lines
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

        .. {}:: 3000, 3001
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
