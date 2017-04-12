#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dropbox


class _Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                _Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass


class DropboxClient(Singleton):
    def __init__(self):
        self.dbx = dropbox.Dropbox(
            'RGvwyNkaMBAAAAAAAAAAF4HNVenKl22UX7gy6GJvqEtPd2D0rnNWzY_157pZxHT0')

    def upload(self, f, path, **kwargs):
        return self.dbx.files_upload(f, path, **kwargs)

    def list(self, path, **kwargs):
        return self.dbx.files_list_folder(path, **kwargs)

    def download(self, path):
        return self.dbx.files_download(path)

    def delete(self, path):
        self.dbx.files_delete(path)
