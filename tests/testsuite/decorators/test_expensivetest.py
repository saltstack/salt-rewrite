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


def test_function_level(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import expensiveTest

    class TestFoo(TestCase):

        @expensiveTest
        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    class TestFoo(TestCase):

        @pytest.mark.expensive_test
        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_expensive_test_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_both_levels(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import expensiveTest

    @expensiveTest
    class TestFoo(TestCase):

        @expensiveTest
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

        @pytest.mark.expensive_test
        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_expensive_test_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
