# -*- coding: utf-8 -*-
"""
    saltrewrite.cli
    ~~~~~~~~~~~~~~~

    ``salt-rewrite``'s CLI interface
"""
import click
from saltrewrite.fixes import Registry


@click.command()
@click.argument(
    "paths", nargs=-1, type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True,)
)
@click.option("--list-fixes", "-l", is_flag=True)
@click.option(
    "--exclude-fix",
    "-E",
    type=click.Choice(Registry.fix_names(), case_sensitive=False),
    multiple=True,
)
@click.option("--interactive/--no-interactive", "-i/-I", is_flag=True, default=True)
def rewrite(paths, interactive, list_fixes, exclude_fix):
    """
    Main CLI entry-point
    """
    if list_fixes:
        click.echo(
            "Fixes:\n{}".format("\n".join(" - {}".format(fix) for fix in Registry.fix_names()))
        )
        return

    with click.progressbar(
        Registry.fixes(exclude_fix), item_show_func=format_progress_bar
    ) as fixes:
        for _, module in fixes:
            module.rewrite(paths, interactive)


def format_progress_bar(item):
    """
    Format a progress bar item
    """
    if item is not None:
        return "Processing {}".format(item[0])
