# pylint: disable=missing-module-docstring,missing-function-docstring,too-many-lines
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_true_with_message_formatted(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertTrue(
                'one',
                msg='The thing why it was skipped is {}'.format(
                    "Blah!"
                )
            )
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert 'one', 'The thing why it was skipped is {}'.format(
                    "Blah!"
                )
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
                1/0
            with self.assertRaises(ZeroDivision) as excinfo:
                1/0
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
                1/0
            with pytest.raises(ZeroDivision) as excinfo:
                1/0
            pytest.raises(CommandExecutionError, self._kernelpkg.remove, release=1)
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
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
                1/0
            with self.assertRaises(ZeroDivision, msg='Blah!') as excinfo:
                1/0
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
                1/0
            with pytest.raises(ZeroDivision) as excinfo:
                1/0
            pytest.raises(CommandExecutionError, self._kernelpkg.remove, release=1)
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_raises_regex_with_statement(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            with self.assertRaisesRegex(ZeroDivision, "division by zero"):
                1/0
            with self.assertRaisesRegex(ZeroDivision, "division by zero") as excinfo:
                1/0
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase
    import pytest

    class TestMe(TestCase):

        def test_one(self):
            with pytest.raises(ZeroDivision, match="division by zero"):
                1/0
            with pytest.raises(ZeroDivision, match="division by zero") as excinfo:
                1/0
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_raises_regex_call(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertRaisesRegex(CommandExecutionError, "error match", self._kernelpkg.remove, release=1)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase
    import pytest

    class TestMe(TestCase):

        def test_one(self):
            pytest.raises(CommandExecutionError, self._kernelpkg.remove, release=1, match="error match")
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_raises_regex_with_message_with_statement(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            with self.assertRaisesRegex(ZeroDivision, "division by zero", msg='Blah!'):
                1/0
            with self.assertRaisesRegex(ZeroDivision, "division by zero", msg='Blah!') as excinfo:
                1/0
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase
    import pytest

    class TestMe(TestCase):

        def test_one(self):
            with pytest.raises(ZeroDivision, match="division by zero"):
                1/0
            with pytest.raises(ZeroDivision, match="division by zero") as excinfo:
                1/0
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_raises_regex_with_message_call(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertRaisesRegex(CommandExecutionError, self._kernelpkg.remove, release=1, match="error match")
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase
    import pytest

    class TestMe(TestCase):

        def test_one(self):
            pytest.raises(CommandExecutionError, self._kernelpkg.remove, release=1, match="error match")
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_dictequal(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertDictEqual({'a': 1}, {'b': 2})
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert {'a': 1} == {'b': 2}
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_setqual(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertSetEqual({'a', 1}, {'b', 2})
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert {'a', 1} == {'b', 2}
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_tupleequal(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertTupleEqual(('a', 1), ('b', 2))
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert ('a', 1) == ('b', 2)
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_listequal(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertListEqual(['a', 1], ['b', 2])
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert ['a', 1] == ['b', 2]
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_sequanceequal(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            self.assertSequenceEqual(['a', 1], ['b', 2])
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            assert ['a', 1] == ['b', 2]
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_multilineequal(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            a = '''
            foo
            '''
            b = '''
            bar
            '''
            self.assertMultiLineEqual(a, b)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            a = '''
            foo
            '''
            b = '''
            bar
            '''
            assert a == b
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_regex(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            pattern = "^foo"
            match = "foo"
            self.assertRegex(match, pattern)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase
    import re

    class TestMe(TestCase):

        def test_one(self):
            pattern = "^foo"
            match = "foo"
            assert re.search(pattern, match)
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code

    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            pattern = "^foo"
            match = "foo"
            self.assertRegex(match, pattern, msg="blah")
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase
    import re

    class TestMe(TestCase):

        def test_one(self):
            pattern = "^foo"
            match = "foo"
            assert re.search(pattern, match), "blah"
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_msg_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code


def test_assert_not_regex(tempfiles):
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            pattern = "^foo"
            match = "foo"
            self.assertNotRegex(match, pattern)
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase
    import re

    class TestMe(TestCase):

        def test_one(self):
            pattern = "^foo"
            match = "foo"
            assert not re.search(pattern, match)
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
    code = textwrap.dedent(
        """
    from unittest import TestCase

    class TestMe(TestCase):

        def test_one(self):
            pattern = "^foo"
            match = "foo"
            self.assertNotRegex(match, pattern, msg="blah")
    """
    )
    expected_code = textwrap.dedent(
        """
    from unittest import TestCase
    import re

    class TestMe(TestCase):

        def test_one(self):
            pattern = "^foo"
            match = "foo"
            assert not re.search(pattern, match), "blah"
    """
    )
    fpath = tempfiles.makepyfile(code, prefix="test_msg_")
    fix_asserts.rewrite(fpath)
    with open(fpath) as rfh:
        new_code = rfh.read()
    assert new_code == expected_code
