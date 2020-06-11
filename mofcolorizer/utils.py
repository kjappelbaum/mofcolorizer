# -*- coding: utf-8 -*-
"""Contextmanagers for the featurization code"""
from __future__ import absolute_import

import contextlib
import os
import shutil
import tempfile


@contextlib.contextmanager
def make_temp_directory():
    """Contextmanager that creates temp dir"""
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)


@contextlib.contextmanager
def temp():
    """Contextmanager that creates temp file"""
    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        yield tmp
    finally:
        tmp.close()  # closes the file, so we can right remove it
        os.remove(tmp.name)
