"""
    saltrewrite.salt.fix_docstrings
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Fix salt docstrings.
"""
# pylint: disable=consider-using-f-string
import re

from bowler import Query
from bowler import TOKEN
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
                file_input<
                    simple_stmt<
                        [STRING]
                        docstring=any*
                    >
                    any*
                >
            |
                class_def=classdef<
                    any*
                    suite<
                        any*
                        simple_stmt<
                            [STRING]
                            docstring=any*
                        >
                        any*
                    >
                    any*
                >
            |
                funcdef<
                    any*
                    suite<
                        any*
                        simple_stmt<
                            [STRING]
                            docstring=any*
                        >
                        any*
                    >
                    any*
                >
            )
            """
        )
        .filter(filter_no_module_docstrings)
        .modify(fix_module_docstrings)
        .execute(write=True, interactive=interactive, silent=silent)
    )


def filter_no_module_docstrings(node, capture, filename):
    """
    If the first child is a docstring, process it
    """
    if "docstring" not in capture:
        # Docstring was not captured, ignore
        return
    if capture["docstring"][0].type != TOKEN.STRING:
        # It's not a docstring, return
        return
    # Process node
    return node


def fix_module_docstrings(node, capture, filename):
    """
    Automaticaly run fixes against docstrings
    """
    # Replace the docstring Leaf value with a fixed docstring
    capture["docstring"][0].value = autofix_docstring(capture["docstring"][0].value, filename)


def autofix_docstring(docstring, filename):
    """
    Run auto fix code against the docstring
    """
    return _convert_version_names_to_numbers(
        _fix_codeblocks(
            _fix_directives_formatting(
                _fix_simple_cli_example_spacing_issues(docstring, filename), filename
            ),
            filename,
        ),
        filename,
    )


CONVERT_VERSION_NAMES_TO_NUMBERS_RE = re.compile(
    r"\.\.(?:[ ]*)?((?P<vtype>(versionadded|versionchanged|deprecated))(?:[:]+)(?:[ ]+)?(?P<version>[^\n]*))"
)


def _handle_convert_version_names_to_numbers_match(match):
    """
    Convert every match with a properly formatted version.
    """
    vtype = match.group("vtype")
    version = match.group("version")
    versions = set()
    splitters = (",", "/", " ")
    for splitter in splitters:
        for _vs in version.split(splitter):
            for _splitter in splitters:
                if _splitter in _vs:
                    break
            else:
                versions.add(_vs.strip())
    parsed_versions = []
    for version in versions:
        try:
            parsed_versions.append(SaltStackVersion.from_name(version))
        except ValueError:
            try:
                parsed_versions.append(SaltStackVersion.parse(version))
            except ValueError as exc:
                raise RuntimeError(f"Unable to parse {version!r} as a SaltStackVersion") from exc

    replace_contents = ".. {}:: {}".format(
        vtype, ",".join([v.string for v in sorted(parsed_versions)])
    )
    return replace_contents


def _convert_version_names_to_numbers(docstring, filename):
    """
    Convert Salt version names to their version numbers counterpart
    """
    return CONVERT_VERSION_NAMES_TO_NUMBERS_RE.sub(
        _handle_convert_version_names_to_numbers_match, docstring
    )


CLI_EXAMPLE_CASE_AND_SPACING_RE = re.compile(
    r"(?:[\n\r]+)([ ]+)CLI Example(?P<plural>s)?(?:[\s]+)?:(?:[^\n\r]+)?(?:[\n\r]+)",
    flags=re.I | re.MULTILINE,
)
CLI_EXAMPLE_MISSING_CODE_BLOCK_RE = re.compile(
    r"\n([ ]+)CLI Example(?P<plural>s)?:\n\n([\s]+)salt ", flags=re.I | re.MULTILINE
)


def _fix_simple_cli_example_spacing_issues(docstring, filename):
    """
    Fix spacing for expected Salt CLI examples
    """
    return CLI_EXAMPLE_MISSING_CODE_BLOCK_RE.sub(
        r"\n\1CLI Example\2:\n\n\1..code-block:: bash\n\n\3salt ",
        CLI_EXAMPLE_CASE_AND_SPACING_RE.sub(r"\n\n\1CLI Example\2:\n\n", docstring),
    )


DIRECTIVES_FORMATTING_RE = re.compile(
    r"(\n(?P<spc1>[ ]+)?((?P<dots>[.]{2,})(?P<spc2>[ ]+)?"
    r"(?P<directive>(?:[^ :]+)))(?:[:]{2})(?P<spc3>[ ]+)?"
    r"(?P<remaining>[^\n]+)?\n)"
)


def _handle_fix_directives_formatting_match(match):
    return (
        "\n{}.. {}:: {}".format(
            match.group("spc1") or "",
            match.group("directive"),
            match.group("remaining") or "",
        ).rstrip()
        + "\n"
    )


def _fix_directives_formatting(docstring, filename):
    """
    Fix directive definition spacing
    """
    return DIRECTIVES_FORMATTING_RE.sub(_handle_fix_directives_formatting_match, docstring)


FIX_CODE_BLOCKS_RE = re.compile(
    r"^(?P<spc1>[ ]+)?(?P<dots>[.]{2}) (?P<directive>code-block)::(?P<lang>.*)\n$"
)


def _fix_codeblocks(docstring, filename):
    """
    Fix expected empty lines around code blocks
    """
    output = []
    found_codeblock = False
    for line in docstring.splitlines(True):
        match = FIX_CODE_BLOCKS_RE.match(line)
        if found_codeblock:
            if line.strip() and line.strip().startswith(":"):
                # code block directive configuration
                output.append(line)
                continue
            if line.strip():
                # We need an empty line after the code-block
                output.append("\n")
            found_codeblock = False
        if match:
            found_codeblock = True
        output.append(line)
    return "".join(output)
