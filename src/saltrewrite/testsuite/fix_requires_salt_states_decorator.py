# -*- coding: utf-8 -*-
"""
    saltrewrite.testsuite.fix_requires_salt_states_decorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Replaces any use of ``@requires_salt_states`` with ``@pytest.mark.requires_salt_states``,
    and, in case ``pytest`` isn't yet imported, it additionall adds the missing
    import
"""
# pylint: disable=no-member
from bowler import Query
from bowler import SYMBOL
from bowler import TOKEN
from fissix.fixer_util import find_indentation
from fissix.fixer_util import Name
from fissix.fixer_util import touch_import
from fissix.pygram import python_symbols as syms
from fissix.pytree import Leaf
from fissix.pytree import Node
from saltrewrite.utils import filter_test_files
from saltrewrite.utils import remove_from_import

MARKER = "pytest.mark.requires_salt_states"
DECORATOR = "requires_salt_states"


def rewrite(paths):
    """
    Rewrite the passed in paths
    """
    # Don't waste time on non-test files
    paths = filter_test_files(paths)
    if not paths:
        return
    (
        Query(paths)
        .select("classdef|funcdef")
        .filter(filter_not_decorated)
        .modify(replace_decorator)
        .write()
    )


def _get_decorator(node):
    """
    Don't modify classes or test methods that aren't decorated with ``DECORATOR``
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

            if str(name) in (DECORATOR, MARKER):
                return decorator


def filter_not_decorated(node, capture, filename):
    """
    Filter undecorated nodes
    """
    return bool(_get_decorator(node))


def replace_decorator(node, capture, filename):
    """
    Replaces usage of ``@requires_salt_states`` with ``@pytest.mark.requires_salt_states``
    """
    indent = find_indentation(node)

    decorator = _get_decorator(node)
    decorator.remove()

    decorator_node = Node(
        SYMBOL.decorator,
        [
            Leaf(TOKEN.AT, "@"),
            Name(MARKER),
        ],
    )
    for child in decorator.children[2:-1]:
        # childen indexing it to remove the initial '@' and '<name>' and final '\n' children
        child.remove()
        if child.type == syms.arglist:
            arglist_node = Node(syms.arglist, [])
            comma = None
            for arg_child in child.children:
                arg_child.remove()
                print(123, repr(arg_child))
                if arg_child.type == syms.atom:
                    # Sometimes instead of passing expanded arguments 'foo(arg1, arg2)' a tuple or a
                    # list is passed as first argument 'foo([arg1, arg2])' or 'foo((arg1, arg2)).
                    # Let's break out of those containers.
                    break_out_of_atom = False
                    comma = None
                    for atom_child in arg_child.children:
                        print(890, atom_child)
                        if atom_child.type not in (
                            syms.listmaker,
                            syms.dictsetmaker,
                            syms.testlist_gexp,
                        ):
                            continue
                        for argument in atom_child.children:
                            argument.remove()
                            arglist_node.append_child(argument)
                            comma = Leaf(TOKEN.COMMA, ",")
                            arglist_node.append_child(comma)
                        break_out_of_atom = True
                        break
                    if break_out_of_atom:
                        continue
                if arg_child.type == TOKEN.COMMA:
                    continue
                arglist_node.append_child(arg_child)
                comma = Leaf(TOKEN.COMMA, ",")
                arglist_node.append_child(comma)
            # Drop the last comma
            if comma is not None:
                comma.remove()
            decorator_node.append_child(arglist_node)
            continue
        elif child.type == syms.atom:
            # Sometimes instead of passing expanded arguments 'foo(arg1, arg2)' a tuple or a
            # list is passed as first argument 'foo([arg1, arg2])' or 'foo((arg1, arg2)).
            # Let's break out of those containers.
            break_out_of_atom = False
            comma = None
            for atom_child in child.children:
                if atom_child.type not in (syms.listmaker, syms.dictsetmaker, syms.testlist_gexp):
                    continue
                for argument in atom_child.children:
                    argument.remove()
                    decorator_node.append_child(argument)
                    comma = Leaf(TOKEN.COMMA, ",")
                    decorator_node.append_child(comma)
                break_out_of_atom = True
                break
            if break_out_of_atom:
                if comma is not None:
                    # Remove last comma
                    comma.remove()
                continue
        decorator_node.append_child(child)
    decorator_node.append_child(Leaf(TOKEN.NEWLINE, "\n"))

    decorated = Node(
        SYMBOL.decorated,
        [decorator_node],
        prefix=decorator.prefix,
    )
    node.replace(decorated)
    decorated.append_child(node)

    if indent is not None:
        node.prefix = indent
    else:
        node.prefix = ""
    touch_import(None, "pytest", node)
    remove_from_import(node, "tests.support.helpers", "requires_salt_states")
