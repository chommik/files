# -*- coding: utf-8 -*-

import unittest
from unittest.mock import MagicMock
from lib.path import Path, Filesystem, VirtualFS, FSObject

# noinspection PyTypeChecker
from lib.path.dummyfs import DummyFSObject, DummyFS
from lib.path.dummyvfs import DummyVirtualFS
from lib.path.virtual_fs import VFSObject

from test_dummyvfs import example_paths, f1, f2


class PathTest(unittest.TestCase):
    # noinspection PyTypeChecker
    def setUp(self):
        self.fs = MagicMock(spec=Filesystem)
        self.vfs = MagicMock(spec=VirtualFS)
        self.fs.exists.return_value = False
        self.vfs.exists.return_value = False
        self.path_mocked = Path(self.fs, self.vfs)

        self.dummyfs = DummyFS({'c1', 'c2', 'c3'})
        self.dummyvfs = DummyVirtualFS(example_paths)
        self.path = Path(self.dummyfs, self.dummyvfs)

    def testIsObject_NonExistent(self):
        self.assertFalse(self.path_mocked.is_object("asdf"))

    def testIsObject_ExistsInFS(self):
        self.fs.exists.return_value = True
        self.assertTrue(self.path_mocked.is_object("asdf"))

    def testIsObject_ExistsInVFS(self):
        self.vfs.exists.return_value = True
        self.assertTrue(self.path_mocked.is_object("asdf"))

    def testFetchObject_NonExistent(self):
        self.assertRaises(FileNotFoundError, self.path_mocked.fetch_object, "asdf")

    def testFetchObject_FromFS(self):
        self.fs.exists.return_value = True
        self.fs.get_object.return_value = DummyFSObject("", "", b"")

        self.assertIsInstance(self.path_mocked.fetch_object("asdf"), FSObject)

    def testFetchObject_FromVFS(self):
        self.vfs.exists.return_value = True

        fs_obj_mock = MagicMock(spec=FSObject)
        self.vfs.get_object.return_value = VFSObject(None, fs_obj_mock)
        self.fs.get_object.return_value = fs_obj_mock

        test_obj_name = "asdf"
        self.assertIsInstance(self.path_mocked.fetch_object(test_obj_name), FSObject)
        self.vfs.get_object.assert_called_once()
        self.fs.get_object.assert_called_once_with(fs_obj_mock)

    def testWalk(self):
        walk_result = list(self.path.walk('/'))

        expected_result = [
            ('/', ['asdf', 'a'], []),
            ('/a', ['b'], []),
            ('/a/b', ['subdir1', 'subdir2', 'subdir3'], [f1, f2]),
            ('/a/b/subdir3', ['sub1', 'sub3', 'sub2'], []),
            ('/a/b/subdir3/sub2', [], []),
            ('/a/b/subdir3/sub3', [], []),
            ('/a/b/subdir3/sub1', [], []),
            ('/a/b/subdir2', [], []),
            ('/a/b/subdir1', [], []),
            ('/asdf', [], [])
        ]

        self.assertCountEqual(((p1, sorted(p2), sorted(p.object_name for p in p3)) for p1, p2, p3 in expected_result),
                              ((p1, sorted(p2), sorted(p.object_name for p in p3)) for p1, p2, p3 in walk_result))