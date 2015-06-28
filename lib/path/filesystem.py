# -*- coding: utf-8 -*-

class FSObject(object):
    pass

class Filesystem(object):
    def exists(self, obj_name: str):
        raise NotImplementedError

    def get_object(self, obj_name: str) -> FSObject:
        raise NotImplementedError
