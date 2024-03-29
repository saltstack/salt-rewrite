"""
    saltrewrite.salt.fix_warn_until
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Fix warn_until calls and replace version names with actual versions.
"""
from bowler import Query
from bowler import TOKEN
from fissix.pytree import Leaf
from saltrewrite.salt.utils import SaltStackVersion


def rewrite(paths, interactive=False, silent=False):
    """
    Rewrite the passed in paths
    """
    (
        Query(paths)
        .select(
            """
            (
                function_call=power<
                    function_name='warn_until'
                    function_parameters=trailer< '(' function_arguments=any* ')' >
                    remainder=any*
                >
            |
                function_call=power<
                    any*
                    trailer< any* >*
                    trailer<
                        '.' function_name='warn_until'
                    >
                    function_parameters=trailer< '(' function_arguments=any* ')' >
                    any*
                >
            )
            """
        )
        .filter(filter_versions)
        .modify(fix_warn_unil_version)
        .execute(write=True, interactive=interactive, silent=silent)
    )


def filter_versions(node, capture, filename):
    """
    If the first child is a docstring, process it
    """
    arglist = capture["function_arguments"][0]
    warn_until_version_argument = arglist.children[0]
    if warn_until_version_argument.type == TOKEN.NUMBER:
        # For example, 3008, 3009.0
        return True
    if warn_until_version_argument.type == TOKEN.STRING:
        # For example, "3008", "Aragon"
        return True
    # Don't process node
    return False


def fix_warn_unil_version(node, capture, filename):
    """
    Automaticaly run fixes against docstrings
    """
    arglist = capture["function_arguments"][0]
    warn_until_version_argument = arglist.children[0]
    if warn_until_version_argument.type == TOKEN.NUMBER:
        salt_version = SaltStackVersion.parse(warn_until_version_argument.value)
    else:
        # Get the value and remove the quotes
        salt_version = SaltStackVersion.parse(warn_until_version_argument.value[1:-1])
    # Replace it with the SaltStackVersion.major attribute
    arglist.children[0] = Leaf(
        TOKEN.NUMBER, str(salt_version.major), prefix=arglist.children[0].prefix
    )
