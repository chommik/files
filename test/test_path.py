# -*- coding: utf-8 -*-

import unittest
from unittest.mock import MagicMock
from lib.path import Path, Filesystem, VirtualFS, FSObject


# noinspection PyTypeChecker
from lib.path.virtual_fs import VFSObject


class PathTest(unittest.TestCase):
    # noinspection PyTypeChecker
    def setUp(self):
        self.fs = MagicMock(spec=Filesystem)
        self.vfs = MagicMock(spec=VirtualFS)

        self.fs.exists.return_value = False
        self.vfs.exists.return_value = False

        self.path = Path(self.fs, self.vfs)

    def testIsObject_NonExistent(self):
        self.assertFalse(self.path.is_object("asdf"))

    def testIsObject_ExistsInFS(self):
        self.fs.exists.return_value = True
        self.assertTrue(self.path.is_object("asdf"))

    def testIsObject_ExistsInVFS(self):
        self.vfs.exists.return_value = True
        self.assertTrue(self.path.is_object("asdf"))

    def testFetchObject_NonExistent(self):
        self.assertRaises(FileNotFoundError, self.path.fetch_object, "asdf")

    def testFetchObject_FromFS(self):
        self.fs.exists.return_value = True
        self.fs.get_object.return_value = FSObject()

        self.assertIsInstance(self.path.fetch_object("asdf"), FSObject)

    def testFetchObject_FromVFS(self):
        self.vfs.exists.return_value = True

        fs_obj_mock = MagicMock(spec=FSObject)
        self.vfs.get_object.return_value = VFSObject(None, fs_obj_mock)
        self.fs.get_object.return_value = fs_obj_mock

        test_obj_name = "asdf"
        self.assertIsInstance(self.path.fetch_object(test_obj_name), FSObject)
        self.vfs.get_object.assert_called_once()
        self.fs.get_object.assert_called_once_with(fs_obj_mock)