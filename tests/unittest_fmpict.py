# coding: utf-8

import unittest
import sys
import os
import shutil

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)
from fmpict.fmpict import FMCTMGenerator


class UnitTestFMPict(unittest.TestCase):
    def setUp(self):
        self._target_dir_path = root_path +  '/fmpict/'
        self._work_dir_path = root_path +  '/tests/worktmp/'
        self._test_dir_path = root_path +  '/tests/fm_sample/'
        if os.path.exists(self._work_dir_path):
            shutil.rmtree(self._work_dir_path)
        os.mkdir(self._work_dir_path)

    
    def testRunningPict(self):
        expect = {u'A': [u'1', u'2', u'3'], u'B': [u'x', u'y', u'z']}
        result = FMCTMGenerator.get_testconditions_from_fmfile(self._test_dir_path + 'simple.mm')

        for key, value in result.items():
            self.assertTrue(key in expect)
            self.assertEqual(set(value), set(expect[key]))
        
if __name__ == '__main__':
    unittest.main()