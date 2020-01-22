# -*- coding: utf-8 -*-
"""
    saltrewrite.cli
    ~~~~~~~~~~~~~~~

    ``salt-rewrite``'s CLI interface
"""
import time

import click
import saltrewrite.testsuite


@click.command()
@click.argument(
    "paths", nargs=-1, type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True,)
)
@click.option("--list-fixes", "-l", is_flag=True)
@click.option("--interactive/--no-interactive", is_flag=True, default=True)
def rewrite(paths, interactive, list_fixes):
    # salt_fixes = []
    # for mod in dir(saltrewrite.salt):
    #    if not mod.startswith('fix_'):
    #        continue
    #    salt_fixes.append(mod)
    test_fixes = []
    for mod in dir(saltrewrite.testsuite):
        if not mod.startswith("fix_"):
            continue
        test_fixes.append(mod)
    if list_fixes:
        # if salt_fixes:
        #    click.echo(
        #        'Salt Fixes:\n{}'.format(
        #            '\n'.join(
        #                ' - {}'.format(fix) for fix in salt_fixes
        #            )
        #        )
        #    )
        if test_fixes:
            click.echo(
                "Tests Fixes:\n{}".format("\n".join(" - {}".format(fix) for fix in test_fixes))
            )
        return

    if test_fixes:
        with click.progressbar(test_fixes, item_show_func=format_progress_bar) as fixes:
            for fixname in fixes:
                fix = getattr(saltrewrite.testsuite, fixname)
                fix.rewrite(paths, interactive)


def format_progress_bar(item):
    if item is not None:
        return "Processing {}".format(item)
