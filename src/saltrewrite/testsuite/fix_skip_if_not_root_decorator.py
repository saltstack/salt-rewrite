# -*- coding: utf-8 -*-
"""
    saltrewrite.testsuite.fix_skip_if_not_root_decorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Replaces any use of ``@skip_if_not_root`` with ``@pytest.mark.skip_if_not_root``,
    and, in case ``pytest`` isn't yet imported, it additionall adds the missing
    import
"""
from bowler import Query
from saltrewrite import utils

MARKER = "pytest.mark.skip_if_not_root"
DECORATOR = "skip_if_not_root"


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
    Replaces usage of ``@skip_if_not_root`` with ``@pytest.mark.skip_if_not_root``
    """
    return utils.rewrite_decorator(node, DECORATOR, MARKER)
