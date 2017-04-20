#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import dropbox
import readline
from six import StringIO
from six.moves import input as raw_input
from clients.singleton import Singleton
from utils import sshr_cfg_path
from webdavlib import WebDav


class WebdavClient(Singleton):
    def __init__(self, **kwargs):
        kwargs.pop('platform')
        self.dav = WebDav(**kwargs)

    @staticmethod
    def init():
        url = raw_input('Your Webdav Address: ')
        path = raw_input('Your Webdav Path: ')
        username = raw_input('Your Webdav Username: ')
        password = raw_input('Your Webdav Password: ')

        cfg = sshr_cfg_path()
        with open(cfg, 'w') as f:
            json.dump({
                'platform': 'webdav',
                'url': url,
                'path': path,
                'username': username,
                'password': password,
            }, f, indent=4)

    def upload(self, data, path, **kwargs):
        hack_fileobj = StringIO(str(data))
        self.dav.upload(path=path, fileobj=hack_fileobj)

    def list(self, path, **kwargs):
        items = self.dav.ls(path)
        return [item.displayname for item in items]

    def download(self, path):
        chunks = ''
        for chunk in self.dav._fetch(path):
            chunks += chunk.decode('utf8')

        content = chunks
        return content

    def delete(self, path):
        self.dav.delete(path)
