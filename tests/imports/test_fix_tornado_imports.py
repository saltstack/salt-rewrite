# -*- coding: utf-8 -*-
import textwrap

from saltrewrite.imports import fix_tornado_imports


def test_module_level_package_import(tempfiles):
    code = textwrap.dedent(
        """
    import tornado
    """
    )
    expected_code = textwrap.dedent(
        """
    import salt.ext.tornado
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_tornado_imports.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_module_level_from_package_import(tempfiles):
    code = textwrap.dedent(
        """
    from tornado import gen
    """
    )
    expected_code = textwrap.dedent(
        """
    from salt.ext.tornado import gen
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_tornado_imports.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_module_level_package_import_usage_renames(tempfiles):
    code = textwrap.dedent(
        """
    import tornado.gen

    def foo():
        raise tornado.gen.Result(None)
    """
    )
    expected_code = textwrap.dedent(
        """
    import salt.ext.tornado.gen

    def foo():
        raise salt.ext.tornado.gen.Result(None)
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_tornado_imports.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_decorator_renames(tempfiles):
    code = textwrap.dedent(
        """
    import tornado.gen

    @tornado.gen
    def foo():
        pass
    """
    )
    expected_code = textwrap.dedent(
        """
    import salt.ext.tornado.gen

    @salt.ext.tornado.gen
    def foo():
        pass
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_tornado_imports.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
