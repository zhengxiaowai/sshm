#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six
import sys

from printer import Console

def check_python():
    if not (six.PY2 or six.PY3):
        Console.error('your python version dont supprot')
        exit()

def exit(code=-1):
    sys.exit(code)
