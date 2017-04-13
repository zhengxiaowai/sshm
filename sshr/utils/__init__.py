#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from six.moves import input as raw_input
from six import PY3, binary_type


def prompt_line(message, default, values):
    inputer = raw_input(message.format(*values))
    inputer = inputer.strip()

    return default if inputer == '' else inputer


def mkdir(path):
    if not (os.path.exists(path) and os.path.isdir(path)):
        os.mkdir(path)


def sshr_cfg_path():
    home_env = os.getenv('HOME', None)
    cfg_path = os.path.join(home_env, '.sshr')
    return cfg_path


def convert_binary_type(string):
    return binary_type(string, 'utf8') if PY3 else binary_type(string)
