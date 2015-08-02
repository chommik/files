# -*- coding: utf-8 -*-
import io

from lib.path import FSObject, Filesystem


class DummyFSObject(FSObject):
    def __init__(self, filename: str, filetype: str, contents: bytes):
        super().__init__(filename, filetype)
        self.buffer = io.BytesIO(contents)

    @property
    def file(self):
        return self.buffer


class DummyFS(Filesystem):
    def __init__(self, files: list):
        super().__init__()
        self.files = files

    def exists(self, obj_name: str):
        return obj_name in (f.filename for f in self.files)

    def get_object(self, obj_name: str) -> FSObject:
        for f in self.files:
            if f.filename == obj_name:
                return f

        raise KeyError(obj_name)

    def list_objects(self) -> set:
        return set(self.files)


