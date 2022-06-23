# pylint: disable=missing-module-docstring,missing-function-docstring
import textwrap

from saltrewrite.testsuite import fix_slow_test_decorator


def test_class_level(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import slowTest

    @slowTest
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    @pytest.mark.slow_test
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_slow_test_decorator.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_function_level(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import slowTest

    class TestFoo(TestCase):

        @slowTest
        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    class TestFoo(TestCase):

        @pytest.mark.slow_test
        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_slow_test_decorator.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_both_levels(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import slowTest

    @slowTest
    class TestFoo(TestCase):

        @slowTest
        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    @pytest.mark.slow_test
    class TestFoo(TestCase):

        @pytest.mark.slow_test
        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_slow_test_decorator.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_multiple_decorators_preserve_order(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import slowTest

    class TestFoo(TestCase):

        @decorator1
        @slowTest
        @decorator2
        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    class TestFoo(TestCase):

        @decorator1
        @pytest.mark.slow_test
        @decorator2
        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_slow_test_decorator.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
