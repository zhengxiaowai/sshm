#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import readline
import qiniu
import requests
from six.moves import input as raw_input
from six.moves.urllib_parse import urljoin
from clients.singleton import Singleton
from utils import sshr_cfg_path


class QiniuClient(Singleton):
    def __init__(self, **kwargs):
        self.access_key = kwargs['access_key']
        self.secert_key = kwargs['secert_key']
        self.bucket_name = kwargs['bucket_name']
        self.domain = kwargs['domain']
        self.q = qiniu.Auth(self.access_key, self.secert_key)

    @staticmethod
    def init():
        access_key = raw_input('Qiniu Access Key: ')
        secert_key = raw_input('Qiniu Secret Key: ')
        bucket_name = raw_input('Qiniu Bucket Name: ')
        domain = raw_input('Qiniu Resource Domain: ')

        cfg = sshr_cfg_path()
        with open(cfg, 'w') as f:
            json.dump({
                'platform': 'qiniu',
                'access_key': access_key,
                'secert_key': secert_key,
                'bucket_name': bucket_name,
                'domain': domain
            }, f, indent=4)

    def upload(self, data, path, **kwargs):
        path = self._wrap_path(path)
        token = self._get_token()
        return qiniu.put_data(token, path, data)

    def list(self, path, **kwargs):
        path = self._wrap_path(path)
        token = self._get_token()
        bucket = qiniu.BucketManager(self.q)

        ret, eof, info = bucket.list(self.bucket_name, 'sshr-', None, None)
        return [item['key'][5:] for item in ret.get('items')]

    def download(self, path):
        path = self._wrap_path(path)
        url = urljoin(self.domain, path)
        private_url = self.q.private_download_url(url, expires=60)
        r = requests.get(private_url)
        return r.text

    def delete(self, path):
        path = self._wrap_path(path)
        token = self._get_token()
        bucket = qiniu.BucketManager(self.q)
        ret, info = bucket.delete(self.bucket_name, path)

    def _get_token(self):
        return self.q.upload_token(self.bucket_name)

    def _wrap_path(self, path):
        return 'sshr-' + path
