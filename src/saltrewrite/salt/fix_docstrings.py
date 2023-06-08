"""
    saltrewrite.salt.fix_docstrings
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @todo: add description
"""
# pylint: disable=consider-using-f-string
import operator
import re
import sys
from collections import namedtuple
from functools import total_ordering

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
                versions.add(_vs)
    parsed_versions = []
    for version in versions:
        try:
            parsed_versions.append(SaltStackVersion.from_name(version))
        except ValueError:
            try:
                parsed_versions.append(SaltStackVersion.parse(version))
            except ValueError as exc:
                raise RuntimeError(f"Unable to parse '{version}' as a SaltStackVersion") from exc

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


# pylint: disable=missing-function-docstring,missing-class-docstring

MAX_SIZE = sys.maxsize
VERSION_LIMIT = MAX_SIZE - 200


@total_ordering
class SaltVersion(namedtuple("SaltVersion", "name, info, released")):  # pragma: no cover
    __slots__ = ()

    def __new__(cls, name, info, released=False):
        if isinstance(info, int):
            info = (info,)
        return super().__new__(cls, name, info, released)

    def __eq__(self, other):
        return self.info == other.info

    def __gt__(self, other):
        return self.info > other.info


class SaltVersionsInfo(type):  # pragma: no cover

    _sorted_versions = ()
    _current_release = None
    _previous_release = None
    _next_release = None

    # ----- Please refrain from fixing whitespace ---------------------------------->
    # The idea is to keep this readable.
    # -------------------------------------------------------------------------------
    # fmt: off
    HYDROGEN      = SaltVersion("Hydrogen"     , info=(2014, 1),  released=True)
    HELIUM        = SaltVersion("Helium"       , info=(2014, 7),  released=True)
    LITHIUM       = SaltVersion("Lithium"      , info=(2015, 5),  released=True)
    BERYLLIUM     = SaltVersion("Beryllium"    , info=(2015, 8),  released=True)
    BORON         = SaltVersion("Boron"        , info=(2016, 3),  released=True)
    CARBON        = SaltVersion("Carbon"       , info=(2016, 11), released=True)
    NITROGEN      = SaltVersion("Nitrogen"     , info=(2017, 7),  released=True)
    OXYGEN        = SaltVersion("Oxygen"       , info=(2018, 3),  released=True)
    FLUORINE      = SaltVersion("Fluorine"     , info=(2019, 2),  released=True)
    NEON          = SaltVersion("Neon"         , info=3000,       released=True)
    SODIUM        = SaltVersion("Sodium"       , info=3001,       released=True)
    MAGNESIUM     = SaltVersion("Magnesium"    , info=3002,       released=True)
    ALUMINIUM     = SaltVersion("Aluminium"    , info=3003,       released=True)
    SILICON       = SaltVersion("Silicon"      , info=3004,       released=True)
    PHOSPHORUS    = SaltVersion("Phosphorus"   , info=3005,       released=True)
    SULFUR        = SaltVersion("Sulfur"       , info=(3006, 0),  released=True)
    CHLORINE      = SaltVersion("Chlorine"     , info=(3007, 0))
    ARGON         = SaltVersion("Argon"        , info=(3008, 0))
    POTASSIUM     = SaltVersion("Potassium"    , info=(3009, 0))
    CALCIUM       = SaltVersion("Calcium"      , info=(3010, 0))
    SCANDIUM      = SaltVersion("Scandium"     , info=(3011, 0))
    TITANIUM      = SaltVersion("Titanium"     , info=(3012, 0))
    VANADIUM      = SaltVersion("Vanadium"     , info=(3013, 0))
    CHROMIUM      = SaltVersion("Chromium"     , info=(3014, 0))
    MANGANESE     = SaltVersion("Manganese"    , info=(3015, 0))
    IRON          = SaltVersion("Iron"         , info=(3016, 0))
    COBALT        = SaltVersion("Cobalt"       , info=(3017, 0))
    NICKEL        = SaltVersion("Nickel"       , info=(3018, 0))
    COPPER        = SaltVersion("Copper"       , info=(3019, 0))
    ZINC          = SaltVersion("Zinc"         , info=(3020, 0))
    GALLIUM       = SaltVersion("Gallium"      , info=(3021, 0))
    GERMANIUM     = SaltVersion("Germanium"    , info=(3022, 0))
    ARSENIC       = SaltVersion("Arsenic"      , info=(3023, 0))
    SELENIUM      = SaltVersion("Selenium"     , info=(3024, 0))
    BROMINE       = SaltVersion("Bromine"      , info=(3025, 0))
    KRYPTON       = SaltVersion("Krypton"      , info=(3026, 0))
    RUBIDIUM      = SaltVersion("Rubidium"     , info=(3027, 0))
    STRONTIUM     = SaltVersion("Strontium"    , info=(3028, 0))
    YTTRIUM       = SaltVersion("Yttrium"      , info=(3029, 0))
    ZIRCONIUM     = SaltVersion("Zirconium"    , info=(3030, 0))
    NIOBIUM       = SaltVersion("Niobium"      , info=(3031, 0))
    MOLYBDENUM    = SaltVersion("Molybdenum"   , info=(3032, 0))
    TECHNETIUM    = SaltVersion("Technetium"   , info=(3033, 0))
    RUTHENIUM     = SaltVersion("Ruthenium"    , info=(3034, 0))
    RHODIUM       = SaltVersion("Rhodium"      , info=(3035, 0))
    PALLADIUM     = SaltVersion("Palladium"    , info=(3036, 0))
    SILVER        = SaltVersion("Silver"       , info=(3037, 0))
    CADMIUM       = SaltVersion("Cadmium"      , info=(3038, 0))
    INDIUM        = SaltVersion("Indium"       , info=(3039, 0))
    TIN           = SaltVersion("Tin"          , info=(3040, 0))
    ANTIMONY      = SaltVersion("Antimony"     , info=(3041, 0))
    TELLURIUM     = SaltVersion("Tellurium"    , info=(3042, 0))
    IODINE        = SaltVersion("Iodine"       , info=(3043, 0))
    XENON         = SaltVersion("Xenon"        , info=(3044, 0))
    CESIUM        = SaltVersion("Cesium"       , info=(3045, 0))
    BARIUM        = SaltVersion("Barium"       , info=(3046, 0))
    LANTHANUM     = SaltVersion("Lanthanum"    , info=(3047, 0))
    CERIUM        = SaltVersion("Cerium"       , info=(3048, 0))
    PRASEODYMIUM  = SaltVersion("Praseodymium" , info=(3049, 0))
    NEODYMIUM     = SaltVersion("Neodymium"    , info=(3050, 0))
    PROMETHIUM    = SaltVersion("Promethium"   , info=(3051, 0))
    SAMARIUM      = SaltVersion("Samarium"     , info=(3052, 0))
    EUROPIUM      = SaltVersion("Europium"     , info=(3053, 0))
    GADOLINIUM    = SaltVersion("Gadolinium"   , info=(3054, 0))
    TERBIUM       = SaltVersion("Terbium"      , info=(3055, 0))
    DYSPROSIUM    = SaltVersion("Dysprosium"   , info=(3056, 0))
    HOLMIUM       = SaltVersion("Holmium"      , info=(3057, 0))
    ERBIUM        = SaltVersion("Erbium"       , info=(3058, 0))
    THULIUM       = SaltVersion("Thulium"      , info=(3059, 0))
    YTTERBIUM     = SaltVersion("Ytterbium"    , info=(3060, 0))
    LUTETIUM      = SaltVersion("Lutetium"     , info=(3061, 0))
    HAFNIUM       = SaltVersion("Hafnium"      , info=(3062, 0))
    TANTALUM      = SaltVersion("Tantalum"     , info=(3063, 0))
    TUNGSTEN      = SaltVersion("Tungsten"     , info=(3064, 0))
    RHENIUM       = SaltVersion("Rhenium"      , info=(3065, 0))
    OSMIUM        = SaltVersion("Osmium"       , info=(3066, 0))
    IRIDIUM       = SaltVersion("Iridium"      , info=(3067, 0))
    PLATINUM      = SaltVersion("Platinum"     , info=(3068, 0))
    GOLD          = SaltVersion("Gold"         , info=(3069, 0))
    MERCURY       = SaltVersion("Mercury"      , info=(3070, 0))
    THALLIUM      = SaltVersion("Thallium"     , info=(3071, 0))
    LEAD          = SaltVersion("Lead"         , info=(3072, 0))
    BISMUTH       = SaltVersion("Bismuth"      , info=(3073, 0))
    POLONIUM      = SaltVersion("Polonium"     , info=(3074, 0))
    ASTATINE      = SaltVersion("Astatine"     , info=(3075, 0))
    RADON         = SaltVersion("Radon"        , info=(3076, 0))
    FRANCIUM      = SaltVersion("Francium"     , info=(3077, 0))
    RADIUM        = SaltVersion("Radium"       , info=(3078, 0))
    ACTINIUM      = SaltVersion("Actinium"     , info=(3079, 0))
    THORIUM       = SaltVersion("Thorium"      , info=(3080, 0))
    PROTACTINIUM  = SaltVersion("Protactinium" , info=(3081, 0))
    URANIUM       = SaltVersion("Uranium"      , info=(3082, 0))
    NEPTUNIUM     = SaltVersion("Neptunium"    , info=(3083, 0))
    PLUTONIUM     = SaltVersion("Plutonium"    , info=(3084, 0))
    AMERICIUM     = SaltVersion("Americium"    , info=(3085, 0))
    CURIUM        = SaltVersion("Curium"       , info=(3086, 0))
    BERKELIUM     = SaltVersion("Berkelium"    , info=(3087, 0))
    CALIFORNIUM   = SaltVersion("Californium"  , info=(3088, 0))
    EINSTEINIUM   = SaltVersion("Einsteinium"  , info=(3089, 0))
    FERMIUM       = SaltVersion("Fermium"      , info=(3090, 0))
    MENDELEVIUM   = SaltVersion("Mendelevium"  , info=(3091, 0))
    NOBELIUM      = SaltVersion("Nobelium"     , info=(3092, 0))
    LAWRENCIUM    = SaltVersion("Lawrencium"   , info=(3093, 0))
    RUTHERFORDIUM = SaltVersion("Rutherfordium", info=(3094, 0))
    DUBNIUM       = SaltVersion("Dubnium"      , info=(3095, 0))
    SEABORGIUM    = SaltVersion("Seaborgium"   , info=(3096, 0))
    BOHRIUM       = SaltVersion("Bohrium"      , info=(3097, 0))
    HASSIUM       = SaltVersion("Hassium"      , info=(3098, 0))
    MEITNERIUM    = SaltVersion("Meitnerium"   , info=(3099, 0))
    DARMSTADTIUM  = SaltVersion("Darmstadtium" , info=(3100, 0))
    ROENTGENIUM   = SaltVersion("Roentgenium"  , info=(3101, 0))
    COPERNICIUM   = SaltVersion("Copernicium"  , info=(3102, 0))
    NIHONIUM      = SaltVersion("Nihonium"     , info=(3103, 0))
    FLEROVIUM     = SaltVersion("Flerovium"    , info=(3104, 0))
    MOSCOVIUM     = SaltVersion("Moscovium"    , info=(3105, 0))
    LIVERMORIUM   = SaltVersion("Livermorium"  , info=(3106, 0))
    TENNESSINE    = SaltVersion("Tennessine"   , info=(3107, 0))
    OGANESSON     = SaltVersion("Oganesson"    , info=(3108, 0))
    # <---- Please refrain from fixing whitespace -----------------------------------
    # The idea is to keep this readable.
    # -------------------------------------------------------------------------------
    # fmt: on

    @classmethod
    def versions(cls):
        if not cls._sorted_versions:
            cls._sorted_versions = sorted(
                (getattr(cls, name) for name in dir(cls) if name.isupper()),
                key=operator.attrgetter("info"),
            )
        return cls._sorted_versions

    @classmethod
    def current_release(cls):
        if cls._current_release is None:
            for version in cls.versions():
                if version.released is False:
                    cls._current_release = version
                    break
        return cls._current_release

    @classmethod
    def next_release(cls):
        if cls._next_release is None:
            next_release_ahead = False
            for version in cls.versions():
                if next_release_ahead:
                    cls._next_release = version
                    break
                if version == cls.current_release():
                    next_release_ahead = True
        return cls._next_release

    @classmethod
    def previous_release(cls):
        if cls._previous_release is None:
            previous = None
            for version in cls.versions():
                if version == cls.current_release():
                    break
                previous = version
            cls._previous_release = previous
        return cls._previous_release


class SaltStackVersion:  # pragma: no cover
    """
    Handle SaltStack versions class.

    Knows how to parse ``git describe`` output, knows about release candidates
    and also supports version comparison.
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

    NAMES = {v.name: v.info for v in SaltVersionsInfo.versions()}
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
        if self.can_have_dot_zero(major):
            minor = minor if minor else 0

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
        if self.can_have_dot_zero(major):
            vnames_key = (major, 0)
        elif self.new_version(major):
            vnames_key = (major,)
        else:
            vnames_key = (major, minor)
        self.name = self.VNAMES.get(vnames_key)
        self.noc = noc
        self.sha = sha

    def new_version(self, major):
        """
        determine if using new versioning scheme
        """
        return bool(int(major) >= 3000 and int(major) < VERSION_LIMIT)

    def can_have_dot_zero(self, major):
        """
        determine if using new versioning scheme
        """
        if int(major) < 3000:
            return True
        return bool(int(major) >= 3006 and int(major) < VERSION_LIMIT)

    @classmethod
    def parse(cls, version_string):
        if version_string.lower() in cls.LNAMES:
            return cls.from_name(version_string)
        vstr = version_string.decode() if isinstance(version_string, bytes) else version_string
        match = cls.git_describe_regex.match(vstr)
        if not match:
            raise ValueError(f"Unable to parse version string: '{version_string}'")
        return cls(*match.groups())

    @classmethod
    def from_name(cls, name):
        if name.lower() not in cls.LNAMES:
            raise ValueError(f"Named version '{name}' is not known")
        return cls(*cls.LNAMES[name.lower()])

    @classmethod
    def current_release(cls):
        return cls(*SaltVersionsInfo.current_release().info)

    @classmethod
    def next_release(cls):
        return cls(*SaltVersionsInfo.next_release().info)

    @property
    def sse(self):
        # Higher than 0.17, lower than first date based
        return 0 < self.major < 2014

    def min_info(self):
        info = [self.major]
        if self.new_version(self.major):
            if self.minor:
                info.append(self.minor)
            elif self.can_have_dot_zero(self.major):
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
            version_string = f"{self.major}"
            if self.minor:
                version_string = f"{self.major}.{self.minor}"
            if not self.minor and self.can_have_dot_zero(self.major):
                version_string = f"{self.major}.{self.minor}"
        else:
            version_string = f"{self.major}.{self.minor}.{self.bugfix}"
        if self.mbugfix:
            version_string += f".{self.mbugfix}"
        if self.pre_type:
            version_string += f"{self.pre_type}{self.pre_num}"
        if self.noc and self.sha:
            noc = self.noc
            if noc < 0:
                noc = "0na"
            version_string += f"+{noc}.{self.sha}"
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
            version_string += f" ({self.RMATCH[(self.major, self.minor)]})"
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
                raise ValueError(f"Cannot instantiate Version from type '{type(other)}'")
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
            parts.append(f"name='{self.name}'")
        parts.extend([f"major={self.major}", f"minor={self.minor}"])

        if self.new_version(self.major):
            if not self.can_have_dot_zero(self.major) and not self.minor:
                parts.remove("".join([x for x in parts if re.search("^minor*", x)]))
        else:
            parts.extend([f"bugfix={self.bugfix}"])

        if self.mbugfix:
            parts.append(f"minor-bugfix={self.mbugfix}")
        if self.pre_type:
            parts.append(f"{self.pre_type}={self.pre_num}")
        noc = self.noc
        if noc == -1:
            noc = "0na"
        if noc and self.sha:
            parts.extend([f"noc={noc}", f"sha={self.sha}"])
        return "<{} {}>".format(self.__class__.__name__, " ".join(parts))


# pylint: enable=missing-function-docstring,missing-class-docstring
