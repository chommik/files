# -*- coding: utf-8 -*-
from io import RawIOBase
from typing import Mapping, Set, Callable
from lib.path import FSObject


class InvalidConversionError(BaseException):
    def __init__(self, type_from, type_to):
        super(InvalidConversionError, self).__init__("Invalid conversion from {} to {}".format(type_from, type_to))


class Handler:
    def __init__(self):
        self.converters = {}

    def register_converter(self, from_type: str, dest_types: Set[str],
                           converter: Callable[[FSObject, str], RawIOBase]) -> None:
        if from_type not in self.converters.keys():
            self.converters[from_type] = {from_type: None}

        for dest_type in dest_types:
            self.converters[from_type][dest_type] = converter

    def supported_types_for(self, object_type: str) -> Set[str]:
        if object_type in self.converters.keys():
            return self.converters[object_type].keys()
        else:
            return {object_type}

    def process_object(self, fsobject: FSObject, target_type: str) -> RawIOBase:
        if target_type not in self.supported_types_for(fsobject.filetype):
            raise InvalidConversionError(fsobject.filetype, target_type)

        if fsobject.filetype == target_type:
            return fsobject.file

        return self.converters[fsobject.filetype][target_type](fsobject, target_type)
