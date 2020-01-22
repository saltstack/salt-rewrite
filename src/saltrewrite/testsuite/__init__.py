# -*- coding: utf-8 -*-
from saltrewrite.testsuite import fix_destructive_test_decorator

__all__ = [modname for modname in list(locals()) if modname.startswith("fix_")]
