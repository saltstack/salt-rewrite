# -*- coding: utf-8 -*-
import functools
import os
import sys
import tempfile
import textwrap

import pytest

IS_DARWIN = sys.platform.lower().startswith("darwin")
if IS_DARWIN and sys.version_info >= (3, 8):
    import multiprocessing

    multiprocessing.set_start_method("fork")


class Tempfiles:
    def __init__(self, request):
        self.request = request

    def makepyfile(self, contents, prefix=None):
        tfile = tempfile.NamedTemporaryFile("w", prefix=prefix, suffix=".py", delete=False)
        tfile.write(textwrap.dedent(contents))
        self.request.addfinalizer(functools.partial(self._delete_temp_file, tfile.name))
        return tfile.name

    def _delete_temp_file(self, fpath):
        if os.path.exists(fpath):
            os.unlink(fpath)


@pytest.fixture
def tempfiles(request):
    return Tempfiles(request)
