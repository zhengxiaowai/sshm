#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hues

class Console(object):

    @staticmethod
    def log(*message):
        hues.log(*message)     

    @staticmethod
    def info(*message):
        hues.info(*message)     

    @staticmethod
    def error(*message):
        hues.error(*message)     

    @staticmethod
    def warn(*message):
        hues.warn(*message)     

    @staticmethod
    def sucess(*message):
        hues.sucess(*message)     
