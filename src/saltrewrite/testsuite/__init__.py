# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring
from saltrewrite.testsuite import fix_asserts
from saltrewrite.testsuite import fix_destructive_test_decorator
from saltrewrite.testsuite import fix_expensive_test_decorator
from saltrewrite.testsuite import fix_slow_test_decorator

__all__ = [modname for modname in list(globals()) if modname.startswith("fix_")]

__fixes__ = [
    (getattr(module, "FIX_PRIORITY", 0), module)
    for module in [globals()[modname] for modname in __all__]
]
