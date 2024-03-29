# pylint: disable=missing-module-docstring,missing-function-docstring
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_skip_if_not_root_decorator.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_skip_if_not_root_decorator.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_skip_if_not_root_decorator.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_multiple_decorators_preserve_order(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import skip_if_not_root

    class TestFoo(TestCase):

        @decorator1
        @skip_if_not_root
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
        @pytest.mark.skip_if_not_root
        @decorator2
        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_skip_if_not_root_decorator.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
