# -*- coding: utf-8 -*-
import tempfile
import textwrap

from saltrewrite.testsuite import fix_expensive_test_decorator


def test_class_level(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import expensiveTest

    @expensiveTest
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    @pytest.mark.expensive_test
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_expensive_test_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
