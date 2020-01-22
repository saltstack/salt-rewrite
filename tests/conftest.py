# -*- coding: utf-8 -*-
import functools
import os
import tempfile
import textwrap

import pytest


class Tempfiles:
    def __init__(self, request):
        self.request = request

    def makepyfile(self, contents):
        tfile = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False)
        tfile.write(textwrap.dedent(contents))
        self.request.addfinalizer(functools.partial(self._delete_temp_file, tfile.name))
        return tfile.name

    def _delete_temp_file(self, fpath):
        if os.path.exists(fpath):
            os.unlink(fpath)


@pytest.fixture
def tempfiles(request):
    return Tempfiles(request)
