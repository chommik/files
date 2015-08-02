# -*- coding: utf-8 -*-
from io import RawIOBase


class FSObject(object):
    def __init__(self, filename: str, filetype: str):
        self.filetype = filetype
        self.filename = filename

    @property
    def file(self) -> RawIOBase:
        raise NotImplementedError


class Filesystem(object):
    def __init__(self):
        pass

    def exists(self, obj_name: str):
        raise NotImplementedError

    def get_object(self, obj_name: str) -> FSObject:
        raise NotImplementedError

    def list_objects(self) -> set:
        raise NotImplementedError
