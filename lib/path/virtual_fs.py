# -*- coding: utf-8 -*-
from collections import namedtuple


class VFSObject(namedtuple('VFSObject_', ['object', 'dest'])):
    pass


class VirtualFS(object):
    def exists(self, path: str):
        raise NotImplementedError

    def isdir(self, path: str):
        raise NotImplementedError

    def isfile(self, path: str):
        raise NotImplementedError

    def get_object(self, path: str) -> VFSObject:
        raise NotImplementedError
