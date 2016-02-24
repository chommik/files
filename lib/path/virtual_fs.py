# -*- coding: utf-8 -*-

from typing import Tuple, Iterable


class VFSObject(object):
    def __init__(self, object_name, dest):
        self.dest = dest
        self.object_name = object_name

    def resolve(self) -> str:
        if isinstance(self.dest, VFSObject):
            return self.dest.resolve()
        else:
            return self.dest


class VirtualFS(object):
    def exists(self, path: str) -> bool:
        raise NotImplementedError

    def isdir(self, path: str) -> bool:
        raise NotImplementedError

    def isfile(self, path: str) -> bool:
        raise NotImplementedError

    def get_object(self, path: str) -> VFSObject:
        raise NotImplementedError

    def list(self, path: str) -> Tuple[Iterable[str], Iterable[str]]:
        """
        Must return tuple in form: (subdirectories, subfiles)
        """
        raise NotImplementedError
