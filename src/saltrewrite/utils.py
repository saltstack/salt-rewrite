# -*- coding: utf-8 -*-
"""
    saltrewrite.utils
    ~~~~~~~~~~~~~~~~~

    @todo: add description
"""
import os

from bowler import TOKEN
from bowler.helpers import find_first
from fissix import fixer_util
from fissix import pygram
from fissix.fixer_util import parenthesize
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
