# -*- coding: utf-8 -*-
import unittest
from lib.path.dummyfs import DummyFSObject, DummyFS


class DummyFSObjectTest(unittest.TestCase):
    def testInit(self):
        DummyFSObject("", "", b"")

    def testFilename(self):
        filename = "test"
        filetype = "asdf"
        fso = DummyFSObject(filename, filetype, b"")
        self.assertEquals(fso.filename, filename)
        self.assertEquals(fso.filetype, filetype)

    def testRead(self):
        file_contents = b"abcdefgh"
        fso = DummyFSObject("", "", file_contents)

        self.assertEquals(fso.file.read(1), file_contents[0].to_bytes(1, byteorder='little'))
        self.assertEquals(fso.file.read(2), file_contents[1:3])
        self.assertEquals(fso.file.read(), file_contents[3:])


class DummyFSTest(unittest.TestCase):
    example_files = [
        DummyFSObject("one", "sometype", b"eno"),
        DummyFSObject("two", "sometype", b""),
        DummyFSObject("three", "sometype", b"somestring")
    ]
    first_file = example_files[0]
    first_file_name = first_file.filename

    def testInit(self):
        DummyFS([])

    def testGetFile(self):
        fs = DummyFS(self.example_files)
        self.assertIs(fs.get_object(self.first_file_name), self.first_file)
        self.assertRaises(KeyError, lambda: fs.get_object("nonexistent"))

    def testExists(self):
        fs = DummyFS(self.example_files)
        self.assertTrue(fs.exists(self.first_file_name))
        self.assertFalse(fs.exists("nonexistent"))

    def testListFiles(self):
        fs = DummyFS(self.example_files)
        all_files = set(self.example_files)
        self.assertEquals(all_files, fs.list_objects())
