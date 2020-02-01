# -*- coding: utf-8 -*-
import operator

from saltrewrite.testsuite import fix_destructive_test_decorator
from saltrewrite.testsuite import fix_expensive_test_decorator

__all__ = [
    module.__name__
    for (priority, module) in sorted(
        [
            (getattr(module, "FIX_PRIORITY", 0), module)
            for module in [
                globals()[modname] for modname in list(globals()) if modname.startswith("fix_")
            ]
        ],
        key=operator.itemgetter(0),
    )
]
