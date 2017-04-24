#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import SSHRAdmin
from ._dropbox import DropboxClient
from ._qiniu import QiniuClient
from ._webdav import WebdavClient

sshr_admin = SSHRAdmin()

sshr_admin.register('dropbox', DropboxClient)
sshr_admin.register('qiniu', QiniuClient)
sshr_admin.register('webdav', WebdavClient)
