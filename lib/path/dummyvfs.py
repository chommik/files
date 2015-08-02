# -*- coding: utf-8 -*-
import os
from lib.path import VirtualFS
from lib.path.virtual_fs import VFSObject


class DummyVirtualFS(VirtualFS):
    def __init__(self, paths):
        """

        @param paths: Paths is a dict in form:
         {
            '/': None
            '/a': None,
            '/a/b': None,
            '/a/b/c1': VFSObject(...),
            '/a/b/c2': VFSObject(...),
            '/asdf': None
         }
         This results in two directories, one with subdirectory containing files, second empty
        """
        self.paths = paths

    def exists(self, path: str):
        return path in self.paths

    def list(self, path: str) -> tuple:
        if not self.isdir(path):
            raise KeyError(path + " is not a directory")

        sub_files = [v for k, v in self.paths.items()
                     if os.path.dirname(k) == path and not self.isdir(k)]
        sub_dirs = [os.path.basename(k) for k, v in self.paths.items()
                    if os.path.dirname(k) == path
                    and not self.isfile(k)
                    and k != path]

        return sub_dirs, sub_files

    def isfile(self, path: str):
        if not self.exists(path):
            raise KeyError(path)
        return self.paths[path] is not None

    def isdir(self, path: str):
        if not self.exists(path):
            raise KeyError(path)
        return self.paths[path] is None

    def get_object(self, path: str) -> VFSObject:
        if not self.exists(path):
            raise KeyError(path)
        if self.paths[path] is None:
            raise ValueError(path + " is a directory")
        return self.paths[path]