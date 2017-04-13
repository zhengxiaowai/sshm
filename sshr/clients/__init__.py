#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import importlib

from glob import glob
from utils import sshr_cfg_path


def get_supported_platform():
    dirname = os.path.dirname(__file__)
    paths = glob(os.path.join(dirname, '_*.py'))

    platforms = []
    for path in paths:
        filename = os.path.basename(path)
        if filename == '__init__.py':
            continue

        sufix = filename.index('.py')
        platforms.append(filename[1: sufix])

    return platforms


def get_client():
    cfg_path = sshr_cfg_path()
    cfg = {}

    with open(cfg_path) as f:
        cfg = json.load(f)
    client_class = _import_client(cfg['platform'])
    return client_class(**cfg)


def init_client(platform):
    client_class = _import_client(platform)
    client_class.init()


def _import_client(platform):
    module_path = 'clients._{}'.format(platform)
    module = importlib.import_module(module_path)
    return getattr(module, '{}{}'.format(platform.capitalize(), 'Client'))
