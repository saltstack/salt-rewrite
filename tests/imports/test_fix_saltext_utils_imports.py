# pylint: disable=missing-module-docstring,missing-function-docstring
import os
import textwrap

from saltrewrite.imports import fix_saltext_utils_imports


def test_module_level_package_import(tempfiles):
    code = textwrap.dedent(
        """
    import salt.utils.args

    def blah():
        salt.utils.args.blah()
    """
    )
    expected_code = textwrap.dedent(
        f"""
    import saltext.{os.environ['SALTEXT_MOD']}.utils.args

    def blah():
        saltext.{os.environ['SALTEXT_MOD']}.utils.args.blah()
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

    def blah():
        args.blah()
    """
    )
    expected_code = textwrap.dedent(
        f"""
    from saltext.{os.environ['SALTEXT_MOD']}.utils import args

    def blah():
        args.blah()
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_saltext_utils_imports.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
