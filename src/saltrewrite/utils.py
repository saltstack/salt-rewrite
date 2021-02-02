# -*- coding: utf-8 -*-
"""
    saltrewrite.utils
    ~~~~~~~~~~~~~~~~~

    @todo: add description
"""
import os

from bowler import SYMBOL
from bowler import TOKEN
from bowler.helpers import find_first
from fissix import fixer_util
from fissix import pygram
from fissix.fixer_util import parenthesize
from fissix.fixer_util import touch_import
from fissix.pygram import python_symbols as syms
from fissix.pytree import Leaf


def get_indent(node):
    """
    Returns the indent for the passed node
    """
    indent = None
    while node:
        indent = find_first(node, TOKEN.INDENT)
        if indent is not None:
            indent = indent.value
            break
        node = node.parent

    return indent


def remove_import(node, name):
    """
    Removes the import.
    """

    # def is_import_stmt(node):
    #    return (
    #        node.type == fixer_util.syms.simple_stmt  # pylint: disable=no-member
    #        and node.children
    #        and fixer_util.is_import(node.children[0])
    #    )

    root = fixer_util.find_root(node)
    if "." in name:
        raise NotImplementedError("Dotted imports not yet supported")

    import_node = fixer_util.find_binding(name, root)
    if import_node:
        import_node.remove()


def get_from_imports(node):
    """
    Return `from module import bar` imports
    """
    from_imports = []
    for child in node.children:
        if child.type != pygram.python_symbols.import_as_names:  # pylint: disable=no-member
            continue
        for leaf in child.children:
            if leaf.type == TOKEN.NAME:
                from_imports.append(leaf)
    return from_imports


def remove_from_import(node, package, name):
    """
    Removes the ``from X import Y`` from the module.
    """

    root = fixer_util.find_root(node)

    import_node = fixer_util.find_binding(name, root, package)
    if not import_node:
        return
    from_imports = get_from_imports(import_node)

    from_imports_children = []
    while from_imports:
        from_import = from_imports.pop(0)
        if from_import.value == name:
            from_import.remove()
            continue
        from_imports_children.append(from_import)

    if not from_imports_children:
        import_node.remove()
        return

    new_import = fixer_util.FromImport(package, from_imports_children)
    import_node.replace(new_import)


def is_multiline(node):
    """
    Checks if node is a multiline string
    """
    if isinstance(node, list):
        return any(is_multiline(n) for n in node)

    for leaf in node.leaves():
        if "\n" in leaf.prefix:
            return True
    return False


def parenthesize_if_necessary(node):
    """
    Parenthesize node if necessary to avoid syntax errors
    """
    if is_multiline(node):
        # If not already parenthesized, parenthesize
        for first_leaf in node.leaves():
            if first_leaf.type in (TOKEN.LPAR, TOKEN.LBRACE, TOKEN.LSQB):
                # Already parenthesized
                return node
            break
        return parenthesize(node.clone())
    return node


def keyword(name, **kwargs):
    """
    A helper to produce keyword nodes
    """
    kwargs.setdefault("prefix", " ")
    return Leaf(TOKEN.NAME, name, **kwargs)


def filter_test_files(paths):
    """
    Filter paths which don't match a salt test module
    """
    if not isinstance(paths, (list, tuple)):
        paths = [paths]
    _paths = []
    for path in paths:
        if not os.path.basename(path).startswith("test_"):
            continue
        _paths.append(path)
    return _paths


def get_decorator(node, decorator_name, marker):
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

            if str(name) in (decorator_name, marker):
                return decorator


def rewrite_decorator(node, decorator_name, marker):
    """
    Replaces usage of ``@<decorator_name>`` with ``@<marker>``
    """
    decorator = get_decorator(node, decorator_name, marker)

    # pylint: disable=no-member

    for leaf in decorator.children:
        if leaf.type == TOKEN.AT:
            continue
        if leaf.type == TOKEN.NAME and leaf.value == decorator_name:
            leaf.value = marker
            continue
        if leaf.type == syms.atom:
            # This scenario is func(*args)
            #
            # Sometimes instead of passing expanded arguments 'foo(arg1, arg2)' a tuple or a
            # list is passed as first argument 'foo([arg1, arg2])' or 'foo((arg1, arg2)).
            # Let's break out of those containers.
            break_out_of_atom = False
            for atom_child in leaf.children:
                if atom_child.type not in (syms.listmaker, syms.dictsetmaker, syms.testlist_gexp):
                    atom_child.remove()
                    continue
                break_out_of_atom = True
                break
            if break_out_of_atom:
                continue
        elif leaf.type == syms.arglist:
            # This scenario is func(*args, **kwargs)
            #
            for arg_child in leaf.children:
                if arg_child.type == syms.atom:
                    # Sometimes instead of passing expanded arguments 'foo(arg1, arg2)' a tuple or a
                    # list is passed as first argument 'foo([arg1, arg2])' or 'foo((arg1, arg2)).
                    # Let's break out of those containers.
                    break_out_of_atom = False
                    for atom_child in arg_child.children:
                        if atom_child.type not in (
                            syms.listmaker,
                            syms.dictsetmaker,
                            syms.testlist_gexp,
                        ):
                            atom_child.remove()
                            continue
                        break_out_of_atom = True
                        break
                    if break_out_of_atom:
                        continue

    # pylint: enable=no-member

    touch_import(None, "pytest", node)
    remove_from_import(node, "tests.support.helpers", decorator_name)
