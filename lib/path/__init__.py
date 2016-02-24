# -*- coding: utf-8 -*-
import os
from lib.path.filesystem import Filesystem, FSObject
from lib.path.virtual_fs import VirtualFS


class Path(object):
    def __init__(self, fs: Filesystem, vfs: VirtualFS):
        self.fs = fs
        self.vfs = vfs

    def exists(self, obj_name):
        return self.fs.exists(obj_name) or self.vfs.exists(obj_name)

    def fetch_object(self, obj_name) -> FSObject:
        if self.fs.exists(obj_name):
            return self.fs.get_object(obj_name)
        elif self.vfs.exists(obj_name):
            vfs_object = self.vfs.get_object(obj_name)
            return self.fs.get_object(vfs_object.resolve())
        else:
            raise FileNotFoundError

    def walk(self, start_path):
        if not self.vfs.exists(start_path):
            raise KeyError(start_path)

        subdirs_to_visit = [start_path]

        while len(subdirs_to_visit) > 0:
            path = subdirs_to_visit.pop()
            subdirs, subfiles = self.vfs.list(path)
            subdirs_to_visit.extend(os.path.join(path, subdir) for subdir in subdirs)
            yield path, subdirs, subfiles
