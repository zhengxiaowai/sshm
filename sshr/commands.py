#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


import six
from prompt_toolkit import prompt


def arg(question, alias):
    def _arg(func):
        @six.wraps(func)
        def __arg(**kwargs):
            kwargs[alias] = prompt(question)
            func(**kwargs)
        return __arg
    return _arg



@arg('HostName: ', 'HostName')
@arg('User: ', 'User')
def add_command(**kwargs):
    print kwargs

    
