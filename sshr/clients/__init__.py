#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from utils import sshr_cfg_path
from .admin import sshr_admin


def get_supported_platform():
    return sshr_admin.clients


def get_client():
    cfg_path = sshr_cfg_path()
    cfg = {}

    with open(cfg_path) as f:
        cfg = json.load(f)
    client = cfg['platform']
    return sshr_admin.get_client(client)


def init_client(platform):
    client_class = sshr_admin.get_client(platform)
    client_class.init()
