# pylint: disable=missing-module-docstring,missing-function-docstring,too-many-lines
import textwrap
from unittest.mock import patch

import pytest
from saltrewrite.salt import fix_dunder_utils


@pytest.fixture(autouse=True)
def _salt_utils_modules(tmp_path):
    modpath = tmp_path / "salt" / "utils" / "foo.py"
    modpath.parent.mkdir(parents=True, exist_ok=True)
    modpath.parent.joinpath("__init__.py").touch()
    code = textwrap.dedent(
        """
        def bar():
            return "BAR FUNC RETURN"
        """
    )
    modpath.write_text(code)
    with patch("saltrewrite.salt.fix_dunder_utils._get_salt_code_root", return_value=tmp_path):
        yield


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
