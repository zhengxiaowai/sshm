#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import importlib

from glob import glob

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
    pass

def init_client(platform):
    module_path = 'clients._{}'.format(platform)
    module = importlib.import_module(module_path)
    client_class = getattr(module, '{}{}'.format(platform.capitalize(), 'Client')) 
    client = client_class()
    client.init()
