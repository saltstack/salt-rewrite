"""
    saltrewrite.salt.fix_docstrings
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @todo: add description
"""
import logging

from bowler import Query
from bowler import SYMBOL
from bowler import TOKEN
from bowler.types import Leaf
from bowler.types import Node
from fissix.fixer_util import Call
from fissix.fixer_util import Dot
from fissix.fixer_util import touch_import

log = logging.getLogger(__name__)


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
        .modify(fix_module_docstrings)
        .execute(write=True, interactive=interactive, silent=silent)
    )


def fix_module_docstrings(node, capture, filename):
    """
    Automaticaly run fixes against docstrings
    """
    if "dunder_mod_func" not in capture:
        return
    dunder_mod_func = capture["dunder_mod_func"][0].value.strip("'").strip('"')
    utils_module, utils_module_funcname = dunder_mod_func.split(".")

    # Make sure we import the right utils module
    touch_import(None, f"salt.utils.{utils_module}", node)
    log.info("Dunder Module Func: %r", dunder_mod_func)

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
                    Leaf(TOKEN.NAME, utils_module, prefix=""),
                    Dot(),
                    call_node,
                ],
            ),
        ],
    )
    # Replace the whole node with the new function call
    node.replace(replacement)


# pylint: enable=missing-function-docstring
