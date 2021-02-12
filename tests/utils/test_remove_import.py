# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring,missing-function-docstring,too-many-lines,redefined-outer-name
import logging
import textwrap

import pytest
from fissix import pygram
from fissix import pytree
from fissix.pgen2.driver import Driver
from saltrewrite.utils import remove_from_import
from saltrewrite.utils import remove_import

log = logging.getLogger(__name__)


@pytest.fixture
def driver():
    return Driver(pygram.python_grammar, convert=pytree.convert, logger=log)


def test_remove_package_import(driver):
    code = textwrap.dedent(
        """
    import foo
    """
    )
    tree = driver.parse_string(code)
    remove_import(tree, "foo")
    assert str(tree).strip() == ""


@pytest.mark.xfail(strict=True)
def test_remove_package_import_dotted(driver):
    code = textwrap.dedent(
        """
    import tests.support.helpers.destructiveTest
    """
    )
    tree = driver.parse_string(code)
    remove_import(tree, "tests.support.helpers.destructiveTest")
    assert str(tree).strip() == ""


def test_remove_from_import_single(driver):
    code = textwrap.dedent(
        """
    from tests.support.helpers import destructiveTest
    """
    )
    tree = driver.parse_string(code)
    remove_from_import(tree, "tests.support.helpers", "destructiveTest")
    assert str(tree).strip() == ""


def test_remove_from_import_multiple(driver):
    code = textwrap.dedent(
        """
    from tests.support.helpers import destructiveTest, dedent
    """
    )
    tree = driver.parse_string(code)
    remove_from_import(tree, "tests.support.helpers", "destructiveTest")
    assert str(tree).strip() == "from tests.support.helpers import dedent"
