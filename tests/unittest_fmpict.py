# coding: utf-8

import unittest
import sys
import os
import shutil

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)
from fmpict import fmpict

class UnitTestFMPict(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._target_dir_path = root_path +  '/fmpict/'
        cls._work_dir_path = root_path +  '/tests/worktmp/'
        cls._test_dir_path = root_path +  '/tests/fm_sample/'
        if os.path.exists(cls._work_dir_path):
            shutil.rmtree(cls._work_dir_path)
        os.mkdir(cls._work_dir_path)

    
    def _testRunningPict(self):
        expect = {u'A': [u'1', u'2', u'3'], u'B': [u'x', u'y', u'z']}
        result = FMCTMGenerator._init_gendata()
        result = FMCTMGenerator.get_testconditions_from_fmfile(self._test_dir_path + 'simple.mm')

        for key, value in result.items():
            self.assertTrue(key in expect)
            self.assertEqual(set(value), set(expect[key]))
    
    def test_get_testconditions_simple(self):
        expect = {u'A': [u'1', u'2', u'3'], u'B': [u'x', u'y', u'z']}
        result = fmpict.get_testconditions(self._test_dir_path + 'simple.mm')
        self.assertTrue(result)
        for key, value in result.items():
            self.assertTrue(key in expect)
            self.assertEqual(set(value), set(expect[key]))        

    def test_run_saveTestConditionFile(self):
        fmpict.run(self._test_dir_path + 'complex_input.mm', False, True, self._work_dir_path + 'savecon.txt', '')
        self.assertTrue(os.path.exists(self._work_dir_path + 'savecon.txt'))

    def test_run_notSaveTestConditionFile(self):
        fmpict.run(self._test_dir_path + 'complex_input.mm', False, False, self._work_dir_path + 'notsavecon.txt', '[dummy]')
        self.assertFalse(os.path.exists(self._work_dir_path + 'notsavecon.txt'))

    def test_run_notRunPict(self):
        fmpict.run(self._test_dir_path + 'complex_input.mm', True, True, self._work_dir_path + 'notrunpict.txt', '')
        self.assertTrue(os.path.exists(self._work_dir_path + 'notrunpict.txt'))

if __name__ == '__main__':
    unittest.main()