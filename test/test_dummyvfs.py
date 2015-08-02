# -*- coding: utf-8 -*-

import unittest
from lib.path.dummyvfs import DummyVirtualFS
from lib.path.virtual_fs import VFSObject

f1 = VFSObject("c1", None)
f2 = VFSObject("c2", None)
example_paths = {
    '/': None,
    '/a': None,
    '/a/b': None,
    '/a/b/c1': f1,
    '/a/b/c2': f2,
    '/a/b/subdir1': None,
    '/a/b/subdir2': None,
    '/a/b/subdir3': None,
    '/a/b/subdir3/sub1': None,
    '/a/b/subdir3/sub2': None,
    '/a/b/subdir3/sub3': None,
    '/asdf': None
}
class DummyVFSTest(unittest.TestCase):
    example_path = "/a/b"
    example_files = [example_paths['/a/b/c1'], example_paths['/a/b/c2']]
    example_dirs = ['subdir1', 'subdir2', 'subdir3']

    def testInit(self):
        DummyVirtualFS(example_paths)

    def testList(self):
        dvs = DummyVirtualFS(example_paths)
        dirs, files = dvs.list(self.example_path)
        self.assertCountEqual(dirs, self.example_dirs)
        self.assertCountEqual(files, self.example_files)

    def testExists(self):
        dvs = DummyVirtualFS(example_paths)
        self.assertTrue(dvs.exists('/a/b'))
        self.assertTrue(dvs.exists('/a/b/c1'))

        self.assertFalse(dvs.exists('/a/nything'))
        self.assertFalse(dvs.exists('/none'))

    def testIsFile(self):
        dvs = DummyVirtualFS(example_paths)
        self.assertTrue(dvs.isfile('/a/b/c1'))
        self.assertFalse(dvs.isfile('/a/b'))
        self.assertRaises(KeyError, lambda: dvs.isfile('/nonexistent'))

    def testIsDir(self):
        dvs = DummyVirtualFS(example_paths)
        self.assertFalse(dvs.isdir('/a/b/c1'))
        self.assertTrue(dvs.isdir('/a/b'))
        self.assertRaises(KeyError, lambda: dvs.isdir('/nonexistent'))

    def testGetObject(self):
        dvs = DummyVirtualFS(example_paths)
        file_path = '/a/b/c1'
        dir_path = '/a/b'
        self.assertIs(dvs.get_object(file_path), example_paths[file_path])
        self.assertRaises(ValueError, lambda: dvs.get_object(dir_path))
