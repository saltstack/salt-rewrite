"""
    saltrewrite.cli
    ~~~~~~~~~~~~~~~

    ``salt-rewrite``'s CLI interface
"""
import click
from saltrewrite.fixes import Registry

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version


@click.command()
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
    ),
)
@click.option("--silent/--no-silent", "-s/-S", is_flag=True, default=False)
@click.option("--interactive/--no-interactive", "-i/-I", is_flag=True, default=False)
@click.option("--list-fixes", "-l", is_flag=True)
@click.option(
    "-fix",
    "-F",
    type=click.Choice(Registry.fix_names(), case_sensitive=False),
    multiple=True,
)
@click.option(
    "--exclude-fix",
    "-E",
    type=click.Choice(Registry.fix_names(), case_sensitive=False),
    multiple=True,
)
@click.version_option(version=version("salt-rewrite"))
def rewrite(paths, interactive, silent, list_fixes, fix, exclude_fix):
    """
    Main CLI entry-point
    """
    if list_fixes:
        click.echo("Fixes:\n{}".format("\n".join(f" - {fix}" for fix in Registry.fix_names())))
        return

    if fix and exclude_fix:
        raise click.UsageError("The --fix and --exclude-fix are mutually exclusive options")

    with click.progressbar(
        Registry.fixes(excluded_names=exclude_fix, only_names=fix),
        item_show_func=format_progress_bar,
    ) as fixes:
        for _, module in fixes:
            module.rewrite(paths, interactive=interactive, silent=silent)


def format_progress_bar(item):
    """
    Format a progress bar item
    """
    if item is not None:
        return f"Processing {item[0]}"
