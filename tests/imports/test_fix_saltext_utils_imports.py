# pylint: disable=missing-module-docstring,missing-function-docstring
import textwrap

from saltrewrite.imports import fix_saltext_utils_imports


def test_module_level_package_import(tempfiles):
    code = textwrap.dedent(
        """
    import salt.utils.args
    """
    )
    expected_code = textwrap.dedent(
        """
    import salt.ext.tornado
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_saltext_utils_imports.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_module_level_from_package_import(tempfiles):
    code = textwrap.dedent(
        """
    from salt.utils import args
    """
    )
    expected_code = textwrap.dedent(
        """
    from salt.ext.tornado import gen
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_saltext_utils_imports.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
