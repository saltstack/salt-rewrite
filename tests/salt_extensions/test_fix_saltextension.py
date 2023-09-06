# pylint: disable=missing-module-docstring,missing-function-docstring
import os
import textwrap

from saltrewrite.salt_extensions import fix_saltext


def test_module_level_package_import(tempfiles):
    if not os.environ.get("SALTEXT_NAME"):
        os.environ["SALTEXT_NAME"] = "docker"

    if not os.environ.get("SALT_MOD"):
        os.environ["SALT_MOD"] = "dockermod"

    code = textwrap.dedent(
        f"""
    import salt.utils.args
    import salt.modules.args
    import salt.utils.{os.environ['SALT_MOD']}.args
    import salt.modules.{os.environ['SALT_MOD']}

    def blah():
        salt.utils.{os.environ['SALT_MOD']}.args.blah()
    """
    )
    expected_code = textwrap.dedent(
        f"""
    import salt.utils.args
    import salt.modules.args
    import saltext.saltext_{os.environ['SALTEXT_NAME']}.utils.{os.environ['SALT_MOD']}.args
    import saltext.saltext_{os.environ['SALTEXT_NAME']}.modules.{os.environ['SALT_MOD']}

    def blah():
        saltext.saltext_{os.environ['SALTEXT_NAME']}.utils.{os.environ['SALT_MOD']}.args.blah()
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_saltext.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_module_level_from_package_import(tempfiles):
    if not os.environ.get("SALTEXT_NAME"):
        os.environ["SALTEXT_NAME"] = "docker"

    if not os.environ.get("SALT_MOD"):
        os.environ["SALT_MOD"] = "dockermod"

    code = textwrap.dedent(
        f"""
    from salt.utils import args
    from salt.utils.{os.environ['SALT_MOD']} import args

    def blah():
        args.blah()
    """
    )
    expected_code = textwrap.dedent(
        f"""
    from salt.utils import args
    from saltext.saltext_{os.environ['SALTEXT_NAME']}.utils.{os.environ['SALT_MOD']} import args

    def blah():
        args.blah()
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_saltext.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_module_level_patch(tempfiles):
    if not os.environ.get("SALTEXT_NAME"):
        os.environ["SALTEXT_NAME"] = "docker"

    if not os.environ.get("SALT_MOD"):
        os.environ["SALT_MOD"] = "dockermod"

    code = textwrap.dedent(
        f"""
    patch_trans_tar = patch(
        "salt.modules.{os.environ['SALT_MOD']}.func",
        fake_func,
    )
    """
    )
    expected_code = textwrap.dedent(
        f"""
    patch_trans_tar = patch(
        "saltext.saltext_{os.environ['SALTEXT_NAME']}.modules.{os.environ['SALT_MOD']}.func",
        fake_func,
    )
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_saltext.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
