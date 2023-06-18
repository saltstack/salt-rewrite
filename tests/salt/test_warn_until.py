# pylint: disable=missing-module-docstring,missing-function-docstring,too-many-lines,consider-using-f-string
import textwrap

from saltrewrite.salt import fix_warn_until


def test_warn_until_func(tempfiles):
    code = textwrap.dedent(
        """
        from salt.utils.versions import warn_until

        def one():
            warn_until("Argon", "Code deprecated in 3008.0")
            print("one")

        def two():
            warn_until(3008, "Code deprecated in 3008.0")
            print("one")

        def three():
            warn_until(3008.0, "Code deprecated in 3008.0")
            print("one")

        def four():
            warn_until("3008", "Code deprecated in 3008.0")
            print("one")
        """
    )
    expected_code = textwrap.dedent(
        """
        from salt.utils.versions import warn_until

        def one():
            warn_until(3008.0, "Code deprecated in 3008.0")
            print("one")

        def two():
            warn_until(3008.0, "Code deprecated in 3008.0")
            print("one")

        def three():
            warn_until(3008.0, "Code deprecated in 3008.0")
            print("one")

        def four():
            warn_until(3008.0, "Code deprecated in 3008.0")
            print("one")
        """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_warn_until.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_warn_until_func_full_import(tempfiles):
    code = textwrap.dedent(
        """
        import salt.utils.versions

        def one():
            salt.utils.versions.warn_until("Argon", "Code deprecated in 3008.0")
            print("one")

        def two():
            salt.utils.versions.warn_until(3008, "Code deprecated in 3008.0")
            print("one")

        def three():
            salt.utils.versions.warn_until(3008.0, "Code deprecated in 3008.0")
            print("one")

        def four():
            salt.utils.versions.warn_until("3008", "Code deprecated in 3008.0")
            print("one")
        """
    )
    expected_code = textwrap.dedent(
        """
        import salt.utils.versions

        def one():
            salt.utils.versions.warn_until(3008.0, "Code deprecated in 3008.0")
            print("one")

        def two():
            salt.utils.versions.warn_until(3008.0, "Code deprecated in 3008.0")
            print("one")

        def three():
            salt.utils.versions.warn_until(3008.0, "Code deprecated in 3008.0")
            print("one")

        def four():
            salt.utils.versions.warn_until(3008.0, "Code deprecated in 3008.0")
            print("one")
        """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_warn_until.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
