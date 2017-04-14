#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import dropbox
import readline
from six.moves import input as raw_input
from clients.singleton import Singleton
from utils import sshr_cfg_path


class DropboxClient(Singleton):
    def __init__(self, **kwargs):
        # RGvwyNkaMBAAAAAAAAAAF4HNVenKl22UX7gy6GJvqEtPd2D0rnNWzY_157pZxHT0
        access_token = kwargs['access_token']
        self.dbx = dropbox.Dropbox(access_token)

    @staticmethod
    def init():
        access_token = raw_input('Dropbox Access Token: ')
        cfg = sshr_cfg_path()
        with open(cfg, 'w') as f:
            json.dump({
                'platform': 'dropbox',
                'access_token': access_token
            }, f, indent=4)

    def upload(self, f, path, **kwargs):
        path = self._wrap_path(path)
        return self.dbx.files_upload(f, path, **kwargs)

    def list(self, path, **kwargs):
        path = self._wrap_path(path)
        c = self.dbx.files_list_folder(path, **kwargs)
        return [ entry.name for entry in c.entries]

    def download(self, path):
        path = self._wrap_path(path)
        _, res = self.dbx.files_download(path)
        return res.content

    def delete(self, path):
        path = self._wrap_path(path)
        self.dbx.files_delete(path)

    def _wrap_path(self, path):
        return  '/' + path

