# -*- coding: utf-8 -*-
from lib.path.filesystem import Filesystem, FSObject
from lib.path.virtual_fs import VirtualFS


class Path(object):
    def __init__(self, fs: Filesystem, vfs: VirtualFS):
        self.fs = fs
        self.vfs = vfs

    def is_object(self, obj_name):
        return self.fs.exists(obj_name) or self.vfs.exists(obj_name)

    def fetch_object(self, obj_name) -> FSObject:
        if self.fs.exists(obj_name):
            return self.fs.get_object(obj_name)
        elif self.vfs.exists(obj_name):
            vfs_object = self.vfs.get_object(obj_name)
            return self.fs.get_object(vfs_object.dest)
        else:
            raise FileNotFoundError
