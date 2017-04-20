#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six

if six.PY3:
    from io import IOBase
    file = (IOBase, six.StringIO)
else:
    file = (file, six.StringIO)
