# -*- coding: utf-8 -*-
"""
    saltrewrite.fixes
    ~~~~~~~~~~~~~~~~~

    Entry point for all the salt rewrite fixes
"""
import operator
from collections import OrderedDict

import saltrewrite.imports
import saltrewrite.testsuite


class RegistryClass(object):

    __slots__ = ("__fixes__",)

    def __init__(self):
        __fixes__ = saltrewrite.imports.__fixes__ + saltrewrite.testsuite.__fixes__
        __sorted_fixes__ = (
            (module.__name__.split(".")[-1], module)
            for (priority, module) in sorted(__fixes__, key=operator.itemgetter(0))
        )
        self.__fixes__ = OrderedDict(__sorted_fixes__)

    def fixes(self, *excluded_names):
        for name in self.__fixes__:
            if name in excluded_names:
                continue
            yield name, self.__fixes__[name]

    def fix_names(self):
        return list(self.__fixes__)


Registry = RegistryClass()
