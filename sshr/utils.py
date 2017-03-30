#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six
import sys
import os
import json

from printer import Console

cfg_filename = '~/.sshr.json'

def check_python():
    if not (six.PY2 or six.PY3):
        Console.error('your python version dont supprot')
        exit()


def check_cfg():
    if not os.path.exists(cfg_filename):
        with open(cfg_filename, 'w') as f:
            json.dump({}, f)

def exit(code=-1):
    sys.exit(code)


def read_cfg():
    cfg = None
    with open(cfg_filename) as f:
        cfg = json.load(f)

    return cfg
