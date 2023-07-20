"""
    saltrewrite.imports.fix_tornado_imports
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Fix tornado imports
"""
# pylint: disable=no-member
import logging
import os
import pathlib

from bowler import Query
from bowler import SYMBOL
from bowler import TOKEN
from fissix.fixer_util import find_indentation
from fissix.fixer_util import Name
from fissix.pytree import Leaf
from fissix.pytree import Node

log = logging.getLogger(__name__)


def rewrite(paths, interactive=False, silent=False):
    """
    Rewrite the passed in paths
    """
    log.warning("PATHS: %s", paths)
    (
        Query(paths)
        .select_module("salt.utils")
        .filter(filter_tornado_imports)
        .rename(f"saltext.{os.environ['SALTEXT_MOD']}.utils")
        #        .select_root()
        #        .select("classdef|funcdef")
        #        .filter(filter_not_decorated)
        #        .modify(replace_decorators)
        .execute(write=True, interactive=interactive, silent=silent)
    )


def filter_tornado_imports(node, capture, filename):
    """
    Filter tornado imports
    """
    log.warning("CAPTURE: %s", capture)
    log.warning("CAPTURE KEYS: %s", list(capture))
    log.warning("MI: %s", capture["module_name"])
    return True
    modname = capture["module_name"].s.split(".")[-1]
    cwd = pathlib.Path.cwd()
    if list(cwd.rglob(f"utils/{modname}.py")):
        return True
    return False


def _get_decorator(node):
    """
    Don't modify classes or test methods that aren't decorated with ``@tornado``
    """
    if node.parent.type == SYMBOL.decorated:
        child = node.parent.children[0]
        if child.type == SYMBOL.decorator:
            decorators = [child]
        elif child.type == SYMBOL.decorators:
            decorators = child.children
        else:
            raise NotImplementedError
        for decorator in decorators:
            name = decorator.children[1]
            assert name.type in {TOKEN.NAME, SYMBOL.dotted_name}

            if str(name).startswith("tornado."):
                return decorator


def filter_not_decorated(node, capture, filename):
    """
    Filter undecorated nodes
    """
    return bool(_get_decorator(node))


def get_decorator_name(decorator):
    """
    Returns the name of the decorator
    """
    name = decorator.children[1]
    assert name.type in {TOKEN.NAME, SYMBOL.dotted_name}
    return str(name)


def replace_decorators(node, capture, filename):
    """
    Replaces usage of ``@tornado.<etc>`` with ``@salt.ext.tornado.<etc>``
    """
    indent = find_indentation(node)

    decorator = _get_decorator(node)
    decorator.remove()

    decorated = Node(
        SYMBOL.decorated,
        [
            Node(
                SYMBOL.decorator,
                [
                    Leaf(TOKEN.AT, "@"),
                    Name(f"salt.ext.{get_decorator_name(decorator)}"),
                    Leaf(TOKEN.NEWLINE, "\n"),
                ],
            )
        ],
        prefix=decorator.prefix,
    )
    node.replace(decorated)
    decorated.append_child(node)

    if indent is not None:
        node.prefix = indent
    else:
        node.prefix = ""
