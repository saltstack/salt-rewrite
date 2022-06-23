# pylint: disable=missing-module-docstring,missing-function-docstring,too-many-lines
import textwrap

from saltrewrite.salt import fix_dunder_utils


def test_fix_call_one_arg(tempfiles):
    code = textwrap.dedent(
        """
    import one.two

    def one():
        one.two.three("four")
        __utils__["foo.bar"]("one")
    """
    )
    expected_code = textwrap.dedent(
        """
    import one.two
    import salt.utils.foo

    def one():
        one.two.three("four")
        salt.utils.foo.bar("one")
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_dunder_utils.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_fix_call_multiple_args(tempfiles):
    code = textwrap.dedent(
        """
    import one.two

    def one():
        one.two.three("four")
        __utils__["foo.bar"]("one", True, 1, 2.0)
    """
    )
    expected_code = textwrap.dedent(
        """
    import one.two
    import salt.utils.foo

    def one():
        one.two.three("four")
        salt.utils.foo.bar("one", True, 1, 2.0)
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_dunder_utils.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_fix_call_keyword_arguments(tempfiles):
    code = textwrap.dedent(
        """
    import one.two

    def one():
        one.two.three("four")
        __utils__["foo.bar"](one="one")
    """
    )
    expected_code = textwrap.dedent(
        """
    import one.two
    import salt.utils.foo

    def one():
        one.two.three("four")
        salt.utils.foo.bar(one="one")
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_dunder_utils.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_fix_call_multiple_keyword_arguments(tempfiles):
    code = textwrap.dedent(
        """
    import one.two

    def one():
        one.two.three("four")
        __utils__["foo.bar"](
            one="one",
            two="two"
        )
    """
    )
    expected_code = textwrap.dedent(
        """
    import one.two
    import salt.utils.foo

    def one():
        one.two.three("four")
        salt.utils.foo.bar(
            one="one",
            two="two")
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_dunder_utils.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_fix_call_mixed(tempfiles):
    code = textwrap.dedent(
        """
    import one.two

    def one():
        one.two.three("four")
        __utils__["foo.bar"]("one", two="two")
    """
    )
    expected_code = textwrap.dedent(
        """
    import one.two
    import salt.utils.foo

    def one():
        one.two.three("four")
        salt.utils.foo.bar("one", two="two")
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_dunder_utils.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
