# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring,missing-function-docstring
import textwrap

from saltrewrite.testsuite import fix_asserts


def test_assert_equal(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertEqual(1, 1)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 == 1
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_equal_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertEqual(1, 1, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 == 1, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_equals(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertEquals(1, 1)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 == 1
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_equals_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertEquals(1, 1, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 == 1, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_fail_unless_equal(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.failUnlessEqual(1, 1)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 == 1
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_fail_unless_equal_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.failUnlessEqual(1, 1, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 == 1, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_not_equal(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertNotEqual(1, 1)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 != 1
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_not_equal_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertNotEqual(1, 1, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 != 1, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_fail_if_equal(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.failIfEqual(1, 1)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 != 1
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_fail_if_equal_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.failIfEqual(1, 1, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 != 1, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_is(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertIs(True, False)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert True is False
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_is_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertIs(True, False, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert True is False, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_is_not(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertIsNot(True, False)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert True is not False
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_is_not_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertIsNot(True, False, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert True is not False, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_in(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertIn(True, [False])
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert True in [False]
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_in_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertIn(True, [False], msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert True in [False], 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_not_in(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertNotIn(True, [False])
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert True not in [False]
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_not_in_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertNotIn(True, [False], msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert True not in [False], 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_true(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertTrue('one')
            self.assert_('one')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 'one'
            assert 'one'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_true_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertTrue('one', msg='Blah')
            self.assert_('one', msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 'one', 'Blah'
            assert 'one', 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_false(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertFalse('one')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert not 'one'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_false_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertFalse('one', msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert not 'one', 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_fail_unless(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.failUnless(False)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert False
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_fail_unless_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.failUnless(False, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert False, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_fail_if(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.failIf(False)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert not False
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_fail_if_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.failIf(False, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert not False, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_is_none(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertIsNone(False)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert False is None
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_is_none_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertIsNone(False, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert False is None, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_is_not_none(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertIsNotNone(False)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert False is not None
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_is_not_none_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertIsNotNone(False, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert False is not None, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_greater(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertGreater(1, 1)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 > 1
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_greater_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertGreater(1, 1, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 > 1, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_greater_equal(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertGreaterEqual(1, 1)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 >= 1
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_greater_equal_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertGreaterEqual(1, 1, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 >= 1, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_less(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertLess(1, 1)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 < 1
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_less_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertLess(1, 1, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 < 1, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_less_equal(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertLessEqual(1, 1)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 <= 1
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_less_equal_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertLessEqual(1, 1, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 1 <= 1, 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_is_instance(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertIsInstance(some_class, object)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert isinstance(some_class, object)
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_is_instance_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertIsInstance(some_class, object, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert isinstance(some_class, object), 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_not_is_instance(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertNotIsInstance(some_class, object)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert not isinstance(some_class, object)
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_not_is_instance_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertNotIsInstance(some_class, object, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert not isinstance(some_class, object), 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_not_almost_equal(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertNotAlmostEqual(1.0545, 1)
            self.assertNotAlmostEqual(1.0545, 1, places=2)
            self.assertNotAlmostEqual(1.0545, 1, delta=1)
            self.assertNotAlmostEqual(1.0545, 1, places=2, delta=1)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase
    import pytest

    class TestMe(TestCase):

        def test_one(self):
            assert 1.0545 != pytest.approx(1, abs=1e-7)
            assert 1.0545 != pytest.approx(1, abs=1e-2)
            assert 1.0545 != pytest.approx(1, abs=1.0)
            assert 1.0545 != pytest.approx(1, abs=1.0)
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_not_almost_equal_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertNotAlmostEqual(1.0545, 1, msg='Blah')
            self.assertNotAlmostEqual(1.0545, 1, places=2, msg='Blah')
            self.assertNotAlmostEqual(1.0545, 1, delta=1, msg='Blah')
            self.assertNotAlmostEqual(1.0545, 1, places=2, delta=1, msg='Blah')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase
    import pytest

    class TestMe(TestCase):

        def test_one(self):
            assert 1.0545 != pytest.approx(1, abs=1e-7), 'Blah'
            assert 1.0545 != pytest.approx(1, abs=1e-2), 'Blah'
            assert 1.0545 != pytest.approx(1, abs=1.0), 'Blah'
            assert 1.0545 != pytest.approx(1, abs=1.0), 'Blah'
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_raises(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            with self.assertRaises(ZeroDivision):
                0/1
            with self.assertRaises(ZeroDivision) as excinfo:
                0/1
            self.assertRaises(CommandExecutionError, self._kernelpkg.remove, release=1)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase
    import pytest

    class TestMe(TestCase):

        def test_one(self):
            with pytest.raises(ZeroDivision):
                0/1
            with pytest.raises(ZeroDivision) as excinfo:
                0/1
            pytest.raises(CommandExecutionError, self._kernelpkg.remove, release=1)
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_raises_with_message(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            with self.assertRaises(ZeroDivision, msg='Blah!'):
                0/1
            with self.assertRaises(ZeroDivision, msg='Blah!') as excinfo:
                0/1
            self.assertRaises(CommandExecutionError, self._kernelpkg.remove, release=1, msg='Blah!')
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase
    import pytest

    class TestMe(TestCase):

        def test_one(self):
            with pytest.raises(ZeroDivision):
                0/1
            with pytest.raises(ZeroDivision) as excinfo:
                0/1
            pytest.raises(CommandExecutionError, self._kernelpkg.remove, release=1)
    """
    )
    fpath = tempfiles.makepyfile(code)
    fix_asserts.rewrite(fpath, False)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
