# -*- coding: utf-8 -*-
"""
    saltrewrite.utils
    ~~~~~~~~~~~~~~~~~

    @todo: add description
"""
from bowler import TOKEN
from bowler.helpers import find_first
from fissix import fixer_util
from fissix import pygram
from fissix.pytree import Leaf
from fissix.pytree import Node


def get_indent(node):
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

    def is_import_stmt(node):
        return (
            node.type == fixer_util.syms.simple_stmt
            and node.children
            and fixer_util.is_import(node.children[0])
        )

    root = fixer_util.find_root(node)
    if "." in name:
        raise NotImplementedError("Dotted imports not yet supported")

    import_node = fixer_util.find_binding(name, root)
    if import_node:
        import_node.remove()


def get_from_imports(node):
    from_imports = []
    for child in node.children:
        if child.type != pygram.python_symbols.import_as_names:
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
