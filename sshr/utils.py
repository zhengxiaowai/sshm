#!/usr/bin/env python
# -*- coding: utf-8 -*-

def prompt_line(message, default, values):
    inputer = raw_input(message.format(*values))
    inputer = inputer.strip()

    return default if inputer == '' else inputer
