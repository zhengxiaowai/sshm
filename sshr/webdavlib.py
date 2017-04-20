#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import requests
import xmltodict
import logging
from _compat import file
from contextlib import closing
from collections import namedtuple
from six.moves.urllib_parse import urlparse, urljoin

__all__ = [
    'WebDav',
    'WebDavError'
]

logger = logging.getLogger('webdav')
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

CHUNK_SIZE_BYTES = 1024 * 1024
ALLOWED_MAX_SIZE_BYTES = CHUNK_SIZE_BYTES * 50

ITEM_ATTRS = [
    'href',
    'lastmodified',
    'contentlength',
    'owner',
    'contenttype',
    'displayname',
    'status'
]

Item = namedtuple('Item', ITEM_ATTRS)


class WebDavError(Exception):
    pass


class WebDav(object):
    def __init__(self, url, port=None, username=None, password=None,
                 verify_ssl=True, path=None, cert=None):
        if port:
            schema = urlparse(url)
            netloc = schema.netloc

            host, port = netloc.split(':')
            port = str(int(port))
            netloc = host + ':' + port
            url = schema._replace(netloc=netloc).geturl()

        if not path.endswith('/'):
            path += '/'

        self.baseurl = urljoin(url, path)
        self.session = requests.session()
        self.session.verify = verify_ssl
        self.session.stream = True

        if username and password:
            self.session.auth = (username, password)

        if cert:
            self.session.cert = cert

    def _request(self, method, path, expected_code, **kwargs):
        if not isinstance(expected_code, (tuple, list)):
            expected_code = [int(expected_code)]

        real_url = urljoin(self.baseurl, path)
        logger.debug(method)
        logger.debug(real_url)
        logger.debug(kwargs)
        response = self.session.request(
            method, real_url, allow_redirects=False, **kwargs)

        logger.debug(response.status_code)
        status_code = response.status_code
        if status_code not in expected_code:
            raise WebDavError('invalid http status code {}, not in {}'.format(
                status_code, str(expected_code)))
        return response

    def _convert_to_list(self, xmljson):
        items = []
        for res in xmljson['d:multistatus']['d:response']:
            attrs = {
                'href': res['d:href'],
                'lastmodified': res['d:propstat']['d:prop']['d:getlastmodified'],
                'contentlength': res['d:propstat']['d:prop']['d:getcontentlength'],
                'owner': res['d:propstat']['d:prop']['d:owner'],
                'contenttype': res['d:propstat']['d:prop']['d:getcontenttype'],
                'displayname': res['d:propstat']['d:prop']['d:displayname'],
                'status': res['d:propstat']['d:status'],
            }
            items.append(Item(**attrs))

        return items

    def ls(self, path=''):
        headers = {'Depth': '1'}
        response = self._request('PROPFIND', path, 207, headers=headers)
        content = xmltodict.parse(response.content)
        items = self._convert_to_list(content)
        return items

    def upload(self, path='', local_path=None, fileobj=None):
        _fileobj = None
        if local_path and os.path.exists(local_path):
            _fileobj = open(local_path, 'rb')
        elif fileobj:
            _fileobj = fileobj

        if isinstance(_fileobj, file):
            # stream upload
            # http://docs.python-requests.org/zh_CN/latest/user/advanced.html#streaming-uploads
            self._request('PUT', path, (200, 201, 204), data=_fileobj)
            _fileobj.close()
        else:
            raise WebDavError('invalid fileobj')

    def _fetch(self, path):
        # stream download
        # http://docs.python-requests.org/zh_CN/latest/user/advanced.html#body-content-workflow
        with closing(self._request('GET', path, 200, stream=True)) as response:
            if int(response.headers['content-length']) > ALLOWED_MAX_SIZE_BYTES:
                for chunk in response.iter_content(CHUNK_SIZE_BYTES):
                    yield chunk
            else:
                yield response.content

    def download(self, path, local_path):
        with open(local_path, 'wb') as f:
            for chunk in self._fetch(path):
                f.write(chunk)

    def delete(self, path):
        self._request('DELETE', path, (204, 404))
        