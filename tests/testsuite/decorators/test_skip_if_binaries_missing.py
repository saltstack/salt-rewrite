# -*- coding: utf-8 -*-
import tempfile
import textwrap

from saltrewrite.testsuite import fix_skip_if_binaries_missing_decorator


def test_class_level(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import skip_if_binaries_missing

    @skip_if_binaries_missing('ps')
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    @pytest.mark.skip_if_binaries_missing('ps')
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_skip_if_binaries_missing_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_function_level(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import skip_if_binaries_missing

    class TestFoo(TestCase):

        @skip_if_binaries_missing('ps')
        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    class TestFoo(TestCase):

        @pytest.mark.skip_if_binaries_missing('ps')
        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_skip_if_binaries_missing_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_both_levels(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import skip_if_binaries_missing

    @skip_if_binaries_missing('ps')
    class TestFoo(TestCase):

        @skip_if_binaries_missing('ps')
        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    @pytest.mark.skip_if_binaries_missing('ps')
    class TestFoo(TestCase):

        @pytest.mark.skip_if_binaries_missing('ps')
        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_skip_if_binaries_missing_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_multiple_binaries_as_arguments(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import skip_if_binaries_missing

    @skip_if_binaries_missing('ps', 'pstree')
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    @pytest.mark.skip_if_binaries_missing('ps', 'pstree')
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_skip_if_binaries_missing_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_multiple_binaries_first_arg_as_list(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import skip_if_binaries_missing

    @skip_if_binaries_missing(['ps', 'pstree'])
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    @pytest.mark.skip_if_binaries_missing('ps', 'pstree')
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_skip_if_binaries_missing_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_multiple_binaries_first_arg_as_tuple(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import skip_if_binaries_missing

    @skip_if_binaries_missing(['ps', 'pstree'])
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    @pytest.mark.skip_if_binaries_missing('ps', 'pstree')
    class TestFoo(TestCase):

        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_skip_if_binaries_missing_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_keyword_arguments(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase
    from tests.support.helpers import skip_if_binaries_missing

    @skip_if_binaries_missing('ps', 'pstree')
    class TestFoo(TestCase):

        def test_one(self):
            assert True

        @skip_if_binaries_missing('git', message='No Git!')
        def test_one(self):
            assert True

        @skip_if_binaries_missing(['python2', 'python3'], check_all=True)
        def test_one(self):
            assert True

        @skip_if_binaries_missing(('python4', 'python5'), check_all=True)
        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    @pytest.mark.skip_if_binaries_missing('ps', 'pstree')
    class TestFoo(TestCase):

        def test_one(self):
            assert True

        @pytest.mark.skip_if_binaries_missing('git', message='No Git!')
        def test_one(self):
            assert True

        @pytest.mark.skip_if_binaries_missing('python2', 'python3', check_all=True)
        def test_one(self):
            assert True

        @pytest.mark.skip_if_binaries_missing('python4', 'python5', check_all=True)
        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_skip_if_binaries_missing_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_pytest_marker_bad_input(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    class TestFoo(TestCase):

        @pytest.mark.skip_if_binaries_missing(('python2', 'python3'), check_all=True)
        def test_one(self):
            assert True

        @pytest.mark.skip_if_binaries_missing(['python4', 'python5'], check_all=True)
        def test_one(self):
            assert True
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    import pytest

    class TestFoo(TestCase):

        @pytest.mark.skip_if_binaries_missing('python2', 'python3', check_all=True)
        def test_one(self):
            assert True

        @pytest.mark.skip_if_binaries_missing('python4', 'python5', check_all=True)
        def test_one(self):
            assert True
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_skip_if_binaries_missing_decorator.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
