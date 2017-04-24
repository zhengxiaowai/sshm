#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SSHRAdmin(object):
    def __init__(self):
        self._client_map = {}

    def register(self, client_name, client_class):
        if client_name not in self._client_map:
            self._client_map[client_name] = client_class

    def get_client(self, client_name):
        return self._client_map.get(client_name, None)
    
    @property
    def clients(self):
        return self._client_map.keys()
        
