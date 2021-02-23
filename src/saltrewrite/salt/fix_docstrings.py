# -*- coding: utf-8 -*-
"""
    saltrewrite.salt.fix_docstrings
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @todo: add description
"""
import re

from bowler import Query
from bowler import TOKEN


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


def _convert_version_names_to_numbers(docstring, filename):
    """
    Convert Salt version names to their version numbers counterpart
    """
    for match in CONVERT_VERSION_NAMES_TO_NUMBERS_RE.finditer(docstring):
        vtype = match.group("vtype")
        version = match.group("version")
        versions = [vs.strip() for vs in version.split(",")]
        parsed_versions = []
        for version in versions:
            try:
                version = SaltStackVersion.from_name(version).string
            except ValueError:
                if version.startswith("v"):
                    try:
                        version = SaltStackVersion.parse(version[1:]).string
                    except ValueError:
                        pass
            parsed_versions.append(version)
        replace_contents = ".. {}:: {}".format(vtype, ",".join(parsed_versions))
        docstring = docstring.replace(match.group(0), replace_contents.rstrip())
    return docstring


CLI_EXAMPLE_CASE_AND_SPACING_RE = re.compile(
    r"(?:[\n]+)([ ]+)CLI Example(?P<plural>s)?(?:[\s]+)?:(?:[^\n]+)?(?:[\n]+)",
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


def _fix_directives_formatting(docstring, filename):
    """
    Fix directive definition spacing
    """
    for match in DIRECTIVES_FORMATTING_RE.finditer(docstring):
        replacement = (
            "\n{}.. {}:: {}".format(
                match.group("spc1") or "",
                match.group("directive"),
                match.group("remaining") or "",
            ).rstrip()
            + "\n"
        )
        docstring = docstring.replace(match.group(0), replacement)
    return docstring


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


# pylint: disable=missing-function-docstring
class SaltStackVersion:
    """
    This is a copy of SaltStackVersion from salt/version.py

    It only exists here as a copy so that we don't need salt to be importable
    to convert version names to version numbers
    """

    __slots__ = (
        "name",
        "major",
        "minor",
        "bugfix",
        "mbugfix",
        "pre_type",
        "pre_num",
        "noc",
        "sha",
    )

    git_sha_regex = r"(?P<sha>g?[a-f0-9]{7,40})"

    git_describe_regex = re.compile(
        r"(?:[^\d]+)?(?P<major>[\d]{1,4})"
        r"(?:\.(?P<minor>[\d]{1,2}))?"
        r"(?:\.(?P<bugfix>[\d]{0,2}))?"
        r"(?:\.(?P<mbugfix>[\d]{0,2}))?"
        r"(?:(?P<pre_type>rc|a|b|alpha|beta|nb)(?P<pre_num>[\d]+))?"
        r"(?:(?:.*)(?:\+|-)(?P<noc>(?:0na|[\d]+|n/a))(?:-|\.)" + git_sha_regex + r")?"
    )
    git_sha_regex = r"^" + git_sha_regex

    git_sha_regex = re.compile(git_sha_regex)

    # Salt versions after 0.17.0 will be numbered like:
    #   <4-digit-year>.<month>.<bugfix>
    #
    # Since the actual version numbers will only be know on release dates, the
    # periodic table element names will be what's going to be used to name
    # versions and to be able to mention them.

    NAMES = {
        # Let's keep at least 3 version names uncommented counting from the
        # latest release so we can map deprecation warnings to versions.
        # ----- Please refrain from fixing PEP-8 E203 and E265 ----->
        # The idea is to keep this readable.
        # -----------------------------------------------------------
        # fmt: off
        "Hydrogen"     : (2014, 1),
        "Helium"       : (2014, 7),
        "Lithium"      : (2015, 5),
        "Beryllium"    : (2015, 8),
        "Boron"        : (2016, 3),
        "Carbon"       : (2016, 11),
        "Nitrogen"     : (2017, 7),
        "Oxygen"       : (2018, 3),
        "Fluorine"     : (2019, 2),
        "Neon"         : (3000,),
        "Sodium"       : (3001,),
        "Magnesium"    : (3002,),
        "Aluminium"    : (3003,),
        "Silicon"      : (3004,),
        "Phosphorus"   : (3005,),
        'Sulfur'       : (3006,),
        'Chlorine'     : (3007,),
        'Argon'        : (3008,),
        'Potassium'    : (3009,),
        'Calcium'      : (3010,),
        'Scandium'     : (3011,),
        'Titanium'     : (3012,),
        'Vanadium'     : (3013,),
        'Chromium'     : (3014,),
        'Manganese'    : (3015,),
        "Iron"         : (3016,),
        "Cobalt"       : (3017,),
        "Nickel"       : (3018,),
        "Copper"       : (3019,),
        "Zinc"         : (3020,),
        "Gallium"      : (3021,),
        "Germanium"    : (3022,),
        "Arsenic"      : (3023,),
        "Selenium"     : (3024,),
        "Bromine"      : (3025,),
        "Krypton"      : (3026,),
        "Rubidium"     : (3027,),
        "Strontium"    : (3028,),
        "Yttrium"      : (3029,),
        "Zirconium"    : (3030,),
        "Niobium"      : (3031,),
        "Molybdenum"   : (3032,),
        "Technetium"   : (3033,),
        "Ruthenium"    : (3034,),
        "Rhodium"      : (3035,),
        "Palladium"    : (3036,),
        "Silver"       : (3037,),
        "Cadmium"      : (3038,),
        "Indium"       : (3039,),
        "Tin"          : (3040,),
        "Antimony"     : (3041,),
        "Tellurium"    : (3042,),
        "Iodine"       : (3043,),
        "Xenon"        : (3044,),
        "Cesium"       : (3045,),
        "Barium"       : (3046,),
        "Lanthanum"    : (3047,),
        "Cerium"       : (3048,),
        "Praseodymium" : (3049,),
        "Neodymium"    : (3050,),
        "Promethium"   : (3051,),
        "Samarium"     : (3052,),
        "Europium"     : (3053,),
        "Gadolinium"   : (3054,),
        "Terbium"      : (3055,),
        "Dysprosium"   : (3056,),
        "Holmium"      : (3057,),
        "Erbium"       : (3058,),
        "Thulium"      : (3059,),
        "Ytterbium"    : (3060,),
        "Lutetium"     : (3061,),
        "Hafnium"      : (3062,),
        "Tantalum"     : (3063,),
        "Tungsten"     : (3064,),
        "Rhenium"      : (3065,),
        "Osmium"       : (3066,),
        "Iridium"      : (3067,),
        "Platinum"     : (3068,),
        "Gold"         : (3069,),
        "Mercury"      : (3070,),
        "Thallium"     : (3071,),
        "Lead"         : (3072,),
        "Bismuth"      : (3073,),
        "Polonium"     : (3074,),
        "Astatine"     : (3075,),
        "Radon"        : (3076,),
        "Francium"     : (3077,),
        "Radium"       : (3078,),
        "Actinium"     : (3079,),
        "Thorium"      : (3080,),
        "Protactinium" : (3081,),
        "Uranium"      : (3082,),
        "Neptunium"    : (3083,),
        "Plutonium"    : (3084,),
        "Americium"    : (3085,),
        "Curium"       : (3086,),
        "Berkelium"    : (3087,),
        "Californium"  : (3088,),
        "Einsteinium"  : (3089,),
        "Fermium"      : (3090,),
        "Mendelevium"  : (3091,),
        "Nobelium"     : (3092,),
        "Lawrencium"   : (3093,),
        "Rutherfordium": (3094,),
        "Dubnium"      : (3095,),
        "Seaborgium"   : (3096,),
        "Bohrium"      : (3097,),
        "Hassium"      : (3098,),
        "Meitnerium"   : (3099,),
        "Darmstadtium" : (3100,),
        "Roentgenium"  : (3101,),
        "Copernicium"  : (3102,),
        "Nihonium"     : (3103,),
        "Flerovium"    : (3104,),
        "Moscovium"    : (3105,),
        "Livermorium"  : (3106,),
        "Tennessine"   : (3107,),
        "Oganesson"    : (3108,),
        # <---- Please refrain from fixing PEP-8 E203 and E265 ------
        # fmt: on
    }

    LNAMES = {k.lower(): v for (k, v) in iter(NAMES.items())}
    VNAMES = {v: k for (k, v) in iter(NAMES.items())}
    RMATCH = {v[:2]: k for (k, v) in iter(NAMES.items())}

    def __init__(
        self,  # pylint: disable=C0103
        major,
        minor=None,
        bugfix=None,
        mbugfix=0,
        pre_type=None,
        pre_num=None,
        noc=0,
        sha=None,
    ):

        if isinstance(major, str):
            major = int(major)

        if isinstance(minor, str):
            if not minor:
                # Empty string
                minor = None
            else:
                minor = int(minor)

        if bugfix is None and not self.new_version(major=major):
            bugfix = 0
        elif isinstance(bugfix, str):
            if not bugfix:
                bugfix = None
            else:
                bugfix = int(bugfix)

        if mbugfix is None:
            mbugfix = 0
        elif isinstance(mbugfix, str):
            mbugfix = int(mbugfix)

        if pre_type is None:
            pre_type = ""
        if pre_num is None:
            pre_num = 0
        elif isinstance(pre_num, str):
            pre_num = int(pre_num)

        if noc is None:
            noc = 0
        elif isinstance(noc, str) and noc in ("0na", "n/a"):
            noc = -1
        elif isinstance(noc, str):
            noc = int(noc)

        self.major = major
        self.minor = minor
        self.bugfix = bugfix
        self.mbugfix = mbugfix
        self.pre_type = pre_type
        self.pre_num = pre_num
        self.name = self.VNAMES.get((major, minor), None)
        if self.new_version(major):
            self.name = self.VNAMES.get((major,), None)
        self.noc = noc
        self.sha = sha

    def new_version(self, major):
        """
        determine if using new versioning scheme
        """
        return bool(int(major) >= 3000 and int(major) < self.NAMES["Oganesson"][0])

    @classmethod
    def parse(cls, version_string):
        if version_string.lower() in cls.LNAMES:
            return cls.from_name(version_string)
        vstr = version_string.decode() if isinstance(version_string, bytes) else version_string
        match = cls.git_describe_regex.match(vstr)
        if not match:
            raise ValueError("Unable to parse version string: '{}'".format(version_string))
        return cls(*match.groups())

    @classmethod
    def from_name(cls, name):
        if name.lower() not in cls.LNAMES:
            raise ValueError("Named version '{}' is not known".format(name))
        return cls(*cls.LNAMES[name.lower()])

    @classmethod
    def from_last_named_version(cls):
        return cls.from_name(
            cls.VNAMES[
                max(
                    [
                        version_info
                        for version_info in cls.VNAMES
                        if version_info[0] < cls.NAMES["Oganesson"][0]
                    ]
                )
            ]
        )

    @classmethod
    def next_release(cls):
        return cls.from_name(
            cls.VNAMES[
                min(
                    [
                        version_info
                        for version_info in cls.VNAMES
                        if version_info > cls.from_last_named_version().info
                    ]
                )
            ]
        )

    @property
    def sse(self):
        # Higher than 0.17, lower than first date based
        return 0 < self.major < 2014

    def min_info(self):
        info = [self.major]
        if self.new_version(self.major):
            if self.minor:
                info.append(self.minor)
        else:
            info.extend([self.minor, self.bugfix, self.mbugfix])
        return info

    @property
    def info(self):
        return tuple(self.min_info())

    @property
    def pre_info(self):
        info = self.min_info()
        info.extend([self.pre_type, self.pre_num])
        return tuple(info)

    @property
    def noc_info(self):
        info = self.min_info()
        info.extend([self.pre_type, self.pre_num, self.noc])
        return tuple(info)

    @property
    def full_info(self):
        info = self.min_info()
        info.extend([self.pre_type, self.pre_num, self.noc, self.sha])
        return tuple(info)

    @property
    def full_info_all_versions(self):
        """
        Return the full info regardless
        of which versioning scheme we
        are using.
        """
        info = [
            self.major,
            self.minor,
            self.bugfix,
            self.mbugfix,
            self.pre_type,
            self.pre_num,
            self.noc,
            self.sha,
        ]
        return tuple(info)

    @property
    def string(self):
        if self.new_version(self.major):
            version_string = "{}".format(self.major)
            if self.minor:
                version_string = "{}.{}".format(self.major, self.minor)
        else:
            version_string = "{}.{}.{}".format(self.major, self.minor, self.bugfix)
        if self.mbugfix:
            version_string += ".{}".format(self.mbugfix)
        if self.pre_type:
            version_string += "{}{}".format(self.pre_type, self.pre_num)
        if self.noc and self.sha:
            noc = self.noc
            if noc < 0:
                noc = "0na"
            version_string += "+{}.{}".format(noc, self.sha)
        return version_string

    @property
    def formatted_version(self):
        if self.name and self.major > 10000:
            version_string = self.name
            if self.sse:
                version_string += " Enterprise"
            version_string += " (Unreleased)"
            return version_string
        version_string = self.string
        if self.sse:
            version_string += " Enterprise"
        if (self.major, self.minor) in self.RMATCH:
            version_string += " ({})".format(self.RMATCH[(self.major, self.minor)])
        return version_string

    @property
    def pre_index(self):
        if self.new_version(self.major):
            pre_type = 2
            if not isinstance(self.minor, int):
                pre_type = 1
        else:
            pre_type = 4
        return pre_type

    def __str__(self):
        return self.string

    def __compare__(self, other, method):
        if not isinstance(other, SaltStackVersion):
            if isinstance(other, str):
                other = SaltStackVersion.parse(other)
            elif isinstance(other, (list, tuple)):
                other = SaltStackVersion(*other)
            else:
                raise ValueError("Cannot instantiate Version from type '{}'".format(type(other)))

        pre_type = self.pre_index
        other_pre_type = other.pre_index
        other_noc_info = list(other.noc_info)
        noc_info = list(self.noc_info)

        if self.new_version(self.major):
            if self.minor and not other.minor:
                # We have minor information, the other side does not
                if self.minor > 0:
                    other_noc_info[1] = 0

            if not self.minor and other.minor:
                # The other side has minor information, we don't
                if other.minor > 0:
                    noc_info[1] = 0

        if self.pre_type and not other.pre_type:
            # We have pre-release information, the other side doesn't
            other_noc_info[other_pre_type] = "zzzzz"

        if not self.pre_type and other.pre_type:
            # The other side has pre-release information, we don't
            noc_info[pre_type] = "zzzzz"

        return method(tuple(noc_info), tuple(other_noc_info))

    def __lt__(self, other):
        return self.__compare__(other, lambda _self, _other: _self < _other)

    def __le__(self, other):
        return self.__compare__(other, lambda _self, _other: _self <= _other)

    def __eq__(self, other):
        return self.__compare__(other, lambda _self, _other: _self == _other)

    def __ne__(self, other):
        return self.__compare__(other, lambda _self, _other: _self != _other)

    def __ge__(self, other):
        return self.__compare__(other, lambda _self, _other: _self >= _other)

    def __gt__(self, other):
        return self.__compare__(other, lambda _self, _other: _self > _other)

    def __repr__(self):
        parts = []
        if self.name:
            parts.append("name='{}'".format(self.name))
        parts.extend(["major={}".format(self.major), "minor={}".format(self.minor)])

        if self.new_version(self.major):
            if not self.minor:
                parts.remove("".join([x for x in parts if re.search("^minor*", x)]))
        else:
            parts.extend(["bugfix={}".format(self.bugfix)])

        if self.mbugfix:
            parts.append("minor-bugfix={}".format(self.mbugfix))
        if self.pre_type:
            parts.append("{}={}".format(self.pre_type, self.pre_num))
        noc = self.noc
        if noc == -1:
            noc = "0na"
        if noc and self.sha:
            parts.extend(["noc={}".format(noc), "sha={}".format(self.sha)])
        return "<{} {}>".format(self.__class__.__name__, " ".join(parts))


# pylint: enable=missing-function-docstring
