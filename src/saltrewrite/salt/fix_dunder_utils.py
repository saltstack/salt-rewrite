"""
    saltrewrite.salt.fix_dunder_utils
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Fix ``__utils__["*.*"](...)`` calls to import and call the real utils module function.
"""
import ast
import os
import pathlib
from functools import lru_cache

import click
from bowler import Query
from bowler import SYMBOL
from bowler import TOKEN
from bowler.types import Leaf
from bowler.types import Node
from fissix.fixer_util import Call
from fissix.fixer_util import Dot
from fissix.fixer_util import touch_import


SALT_DUNDERS = (
    "__active_provider_name__",
    "__context__",
    "__env__",
    "__events__",
    "__executors__",
    "__grains__",
    "__instance_id__",
    "__jid_event__",
    "__low__",
    "__lowstate__",
    "__master_opts__",
    "__opts__",
    "__pillar__",
    "__proxy__",
    "__reg__",
    "__ret__",
    "__runner__",
    "__running__",
    "__salt__",
    "__salt_system_encoding__",
    "__serializers__",
    "__states__",
    "__utils__",
)


class DunderParser(ast.NodeTransformer):  # pylint: disable=missing-class-docstring
    # pylint: disable=missing-function-docstring,invalid-name
    def __init__(self):
        self.virtualname = None
        self.uses_salt_dunders = False

    def visit_Name(self, node):
        if node.id in SALT_DUNDERS:
            self.uses_salt_dunders = True

    def visit_Assign(self, node):
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            if target.id == "__virtualname__":
                self.virtualname = node.value.s

    # pylint: enable=missing-function-docstring,invalid-name


def _get_salt_code_root():
    return pathlib.Path.cwd()


@lru_cache
def get_utils_module_info():
    """
    Collect utils modules dunder information.
    """
    mapping = {}
    salt_utils_package_path = _get_salt_code_root().joinpath("salt", "utils")
    for path in salt_utils_package_path.rglob("*.py"):
        transformer = DunderParser()
        tree = ast.parse(path.read_text())
        transformer.visit(tree)
        mapping[path.resolve()] = {
            "modname": path.stem,
            "virtualname": transformer.virtualname or path.stem,
            "uses_salt_dunders": transformer.uses_salt_dunders,
        }
    return mapping


@lru_cache
def get_utils_module_details(name):
    """
    Return utils module details.
    """
    full_module_name = f"salt.utils.{name}"
    full_module_path = pathlib.Path(f"{full_module_name.replace('.', os.sep)}.py")
    utils_module_info = get_utils_module_info()
    if full_module_path.exists():
        return utils_module_info[full_module_path]
    modname = name.split(".")[0]
    for entry in utils_module_info.values():
        if entry["virtualname"] == modname:
            return entry
    raise RuntimeError(
        f"Could not find the python module for {name!r} and '{full_module_path}' " "does not exist"
    )


def rewrite(paths, interactive=False, silent=False):
    """
    Rewrite the passed in paths
    """
    (
        Query(paths)
        .select(
            """
            (
                dunder_call=power<
                    '__utils__'
                    trailer< '[' dunder_mod_func=any* ']' >
                    trailer< '(' function_arguments=any* ')' >
                >

            )
            """
        )
        .modify(fix_dunder_utils_calls)
        .execute(write=True, interactive=interactive, silent=silent)
    )


def fix_dunder_utils_calls(node, capture, filename):
    """
    Automatically rewrite dunder utils calls to call the module directly.
    """
    if "dunder_mod_func" not in capture:
        return
    dunder_mod_func = capture["dunder_mod_func"][0].value.strip("'").strip('"')

    utils_module, utils_module_funcname = dunder_mod_func.split(".")
    details = get_utils_module_details(utils_module)
    if details["uses_salt_dunders"]:

        click.echo(
            f" * Not calling 'salt.utils.{details['modname']}.{utils_module_funcname}' "
            f"directly because internally the 'salt.utils.{details['modname']}' "
            "module uses salt dunders",
            err=True,
        )
        return

    # Make sure we import the right utils module
    touch_import(None, f"salt.utils.{details['modname']}", node)
    click.echo(f" * Fixing dunder module func call: '{dunder_mod_func}'")

    # Un-parent the function arguments so we can add them to a new call
    for leaf in capture["function_arguments"]:
        leaf.parent = None

    # Create the new function call
    call_node = Call(
        Leaf(TOKEN.NAME, utils_module_funcname, prefix=""),
        capture["function_arguments"],
    )

    # Create replacement node
    replacement = Node(
        SYMBOL.power,
        [
            Leaf(TOKEN.NAME, "salt", prefix=capture["node"].prefix),
            Node(
                SYMBOL.trailer,
                [
                    Dot(),
                    Leaf(TOKEN.NAME, "utils", prefix=""),
                    Dot(),
                    Leaf(TOKEN.NAME, details["modname"], prefix=""),
                    Dot(),
                    call_node,
                ],
            ),
        ],
    )
    # Replace the whole node with the new function call
    node.replace(replacement)


# pylint: enable=missing-function-docstring
