# -*- coding: utf-8 -*-

import unittest
from io import RawIOBase, BytesIO
from lib.handler import Handler, InvalidConversionError
from lib.path import FSObject
from lib.path.dummyfs import DummyFSObject


def dummy_converter(fsobject: FSObject, to_type: str) -> RawIOBase:
    return BytesIO(to_type.encode() + fsobject.file.read())


class HandlerTest(unittest.TestCase):
    content = b"SOME_CONTENT"

    from_type = 'f1'
    to_types = {'f2', 'f3', 'f4'}

    type_to_register = "some_non_existent_type"

    def setUp(self):
        self.handler = Handler()
        self.handler.register_converter(self.from_type, self.to_types, dummy_converter)

    def testIdentitySupported(self):
        some_type = "SOMETYPE"
        self.assertIn(some_type, self.handler.supported_types_for(some_type))

    def testRegisterConverter(self):
        with self.assertRaises(InvalidConversionError):
            fsobject = DummyFSObject("FILE_NAME", self.type_to_register, self.content)
            self.handler.process_object(fsobject, 'anything')

        self.handler.register_converter(self.type_to_register, self.to_types, dummy_converter)

        fsobject = DummyFSObject("FILE_NAME", self.type_to_register, self.content)
        self.handler.process_object(fsobject, self.type_to_register)
        self.handler.process_object(fsobject, next(iter(self.to_types)))

    def testIdentity(self):
        some_type = "SOME_TYPE"
        fsobject = DummyFSObject("FILE_NAME", some_type, self.content)
        converted_object = self.handler.process_object(fsobject, some_type)
        converted_content = converted_object.read()
        self.assertEquals(self.content, converted_content)

    def testConversion(self):
        for destination_type in self.to_types:
            fsobject = DummyFSObject("FILE_NAME", self.from_type, self.content)
            converted_object = self.handler.process_object(fsobject, destination_type)
            converted_content = converted_object.read()
            self.assertEquals(converted_content, destination_type.encode() + self.content)

    def testInvalidConversion(self):
        with self.assertRaises(InvalidConversionError):
            fsobject = DummyFSObject("", "f2", self.content)
            self.handler.process_object(fsobject, 'this_does_not_exist')
