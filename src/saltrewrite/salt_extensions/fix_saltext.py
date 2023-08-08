"""
    saltrewrite.salt_extensions.fix_saltext
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Fix imports and module references
    when migrating Salt modules to extensions
"""
# pylint: disable=no-member
import logging
import os
import re

from bowler import Query

log = logging.getLogger(__name__)


def rewrite(paths, interactive=False, silent=False):
    """
    Rewrite the passed in paths
    """
    if "SALTEXT_NAME" in os.environ:
        log.warning("PATHS: %s", paths)
        (
            Query(paths)
            .select_module("tests.support.mock")
            .rename("unittest.mock")
            .select_module("salt.utils")
            .filter(filter_salt_imports)
            .rename(f"saltext.saltext_{os.environ['SALTEXT_NAME']}.utils")
            .select_root()
            .select_module("salt.modules")
            .filter(filter_salt_imports)
            .rename(f"saltext.saltext_{os.environ['SALTEXT_NAME']}.modules")
            .select_module("salt.states")
            .filter(filter_salt_imports)
            .rename(f"saltext.saltext_{os.environ['SALTEXT_NAME']}.states")
            .select_root()
            .select_function("patch")
            .filter(filter_salt_imports)
            .modify(replace_patch_arglist)
            .execute(write=True, interactive=interactive, silent=silent)
        )


def filter_salt_imports(node, capture, filename):
    """
    Filter salt imports
    """
    if (
        f"salt.utils.{os.environ['SALTEXT_NAME']}" in f"{capture['node']}"
        or f"salt.states.{os.environ['SALTEXT_NAME']}" in f"{capture['node']}"
        or f"salt.modules.{os.environ['SALTEXT_NAME']}" in f"{capture['node']}"
        or f"from salt.modules import {os.environ['SALTEXT_NAME']}" in f"{capture['node']}"
        or f"from salt.states import {os.environ['SALTEXT_NAME']}" in f"{capture['node']}"
        or f"from salt.utils import {os.environ['SALTEXT_NAME']}" in f"{capture['node']}"
    ):
        return True
    return False


def replace_patch_arglist(node, capture, filename):
    """
    Replaces instances of salt.modules and salt.utils for salt extensions
    """
    mod_sub_pattern = "salt.modules"
    mod_sub_repl = f"saltext.saltext_{os.environ['SALTEXT_NAME']}.modules"

    util_sub_pattern = "salt.utils"
    util_sub_repl = f"saltext.saltext_{os.environ['SALTEXT_NAME']}.utils"

    if hasattr(node, "children"):
        for child in node.children:
            if hasattr(child, "children"):
                for _child in child.children:
                    if hasattr(_child, "children"):
                        for __child in _child.children:
                            if hasattr(__child, "value"):
                                if os.environ["SALTEXT_NAME"] in __child.value:
                                    __child.value = re.sub(
                                        mod_sub_pattern, mod_sub_repl, __child.value
                                    )
                                    __child.value = re.sub(
                                        util_sub_pattern, util_sub_repl, __child.value
                                    )
                    else:
                        if hasattr(_child, "value"):
                            if os.environ["SALTEXT_NAME"] in _child.value:
                                _child.value = re.sub(mod_sub_pattern, mod_sub_repl, _child.value)
                                _child.value = re.sub(util_sub_pattern, util_sub_repl, _child.value)
            else:
                if hasattr(child, "value"):
                    if os.environ["SALTEXT_NAME"] in child.value:
                        child.value = re.sub(mod_sub_pattern, mod_sub_repl, child.value)
                        child.value = re.sub(util_sub_pattern, util_sub_repl, child.value)
