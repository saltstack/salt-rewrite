"""
    saltrewrite.testsuite.fix_destructive_test_decorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Replaces any use of ``@destructiveTest`` with ``@pytest.mark.destructive_test``,
    and, in case ``pytest`` isn't yet imported, it additionall adds the missing
    import
"""
from bowler import Query
from saltrewrite import utils

MARKER = "pytest.mark.destructive_test"
DECORATOR = "destructiveTest"


def rewrite(paths, interactive=False, silent=False):
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
        .execute(write=True, interactive=interactive, silent=silent)
    )


def filter_not_decorated(node, capture, filename):
    """
    Filter undecorated nodes
    """
    return bool(utils.get_decorator(node, DECORATOR, MARKER))


def replace_decorator(node, capture, filename):
    """
    Replaces usage of ``@destructiveTest`` with ``@pytest.mark.destructive_test``
    """
    return utils.rewrite_decorator(node, DECORATOR, MARKER)
