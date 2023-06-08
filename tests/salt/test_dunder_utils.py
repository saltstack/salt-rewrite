# pylint: disable=missing-module-docstring,missing-function-docstring,too-many-lines,redefined-outer-name
import logging
import textwrap
from unittest.mock import patch

import pytest
from saltrewrite.salt import fix_dunder_utils

log = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def salt_utils_package(tmp_path):
    package_path = tmp_path / "salt" / "utils"
    modpath = package_path / "foo.py"
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
        yield package_path


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


@pytest.mark.parametrize("salt_dunder", fix_dunder_utils.SALT_DUNDERS)
def test_unsafe_utils_call_not_rewritten(tempfiles, salt_utils_package, salt_dunder):
    unsafe_modpath = salt_utils_package / "unsafe.py"
    modcode = textwrap.dedent(
        f"""
        def bar(one, two=None):
            return {salt_dunder}["bar"](two=two)
        """
    )
    log.info("Generated utils module:\n>>>>>%s<<<<<", modcode)
    unsafe_modpath.write_text(modcode)
    code = textwrap.dedent(
        """
    import one.two

    def one():
        one.two.three("four")
        __utils__["unsafe.bar"]("one", two="two")
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_dunder_utils.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == code
