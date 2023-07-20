# pylint: disable=missing-module-docstring
from saltrewrite.imports import fix_saltext_utils_imports
from saltrewrite.imports import fix_tornado_imports

__all__ = [modname for modname in list(globals()) if modname.startswith("fix_")]

__fixes__ = [
    (getattr(module, "FIX_PRIORITY", 0), module)
    for module in [globals()[modname] for modname in __all__]
]
