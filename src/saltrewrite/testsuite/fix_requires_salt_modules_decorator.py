# -*- coding: utf-8 -*-
"""
    saltrewrite.testsuite.fix_requires_salt_modules_decorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Replaces any use of ``@requires_salt_modules`` with ``@pytest.mark.requires_salt_modules``,
    and, in case ``pytest`` isn't yet imported, it additionall adds the missing
    import
"""
from bowler import Query
from saltrewrite import utils

MARKER = "pytest.mark.requires_salt_modules"
DECORATOR = "requires_salt_modules"


def rewrite(paths):
    """
    Rewrite the passed in paths
    """
    # Don't waste time on non-test files
    paths = utils.filter_test_files(paths)
    if not paths:
        return
    (
        Query(paths)
        .select("classdef|funcdef")
        .filter(filter_not_decorated)
        .modify(replace_decorator)
        .write()
    )


def filter_not_decorated(node, capture, filename):
    """
    Filter undecorated nodes
    """
    return bool(utils.get_decorator(node, DECORATOR, MARKER))


def replace_decorator(node, capture, filename):
    """
    Replaces usage of ``@requires_salt_modules`` with ``@pytest.mark.requires_salt_modules``
    """
    return utils.rewrite_decorator(node, DECORATOR, MARKER)
