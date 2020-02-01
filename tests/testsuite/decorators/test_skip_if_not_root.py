# -*- coding: utf-8 -*-
import textwrap

from saltrewrite.testsuite import fix_skip_if_not_root_decorator


def test_class_level(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import skip_if_not_root

    @skip_if_not_root
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    @pytest.mark.skip_if_not_root
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_skip_if_not_root_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_function_level(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import skip_if_not_root

    class TestFoo(TestCase):

        @skip_if_not_root
        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    class TestFoo(TestCase):

        @pytest.mark.skip_if_not_root
        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_skip_if_not_root_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_both_levels(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import skip_if_not_root

    @skip_if_not_root
    class TestFoo(TestCase):

        @skip_if_not_root
        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    @pytest.mark.skip_if_not_root
    class TestFoo(TestCase):

        @pytest.mark.skip_if_not_root
        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_skip_if_not_root_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
