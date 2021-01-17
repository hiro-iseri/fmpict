# coding: utf-8

import unittest
import sys
import os
import subprocess
import shutil

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)
import fmpict


class TestFMPict(unittest.TestCase):
    def setUp(self):
        self._target_dir_path = root_path +  '/fmpict/'
        self._work_dir_path = root_path +  '/tests/worktmp/'
        self._test_dir_path = root_path +  '/tests/fm_sample/'
        if os.path.exists(self._work_dir_path):
            shutil.rmtree(self._work_dir_path)
        os.mkdir(self._work_dir_path)
    
    def testRunningPict(self):
        self.assertEqual(True, True)
        os.chdir(self._work_dir_path)
        command = r'python %sfmpict.py %ssimple.mm' % (self._target_dir_path, self._test_dir_path)
        out_proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout_data, stderr_data = out_proc.communicate()
        out_proc.wait()

        self.assertFalse(stderr_data)
        expected_output = b'A\tB\n3\tx\n3\tz\n1\tx\n1\ty\n2\tx\n3\ty\n1\tz\n2\tz\n2\ty\n'
        stdout_data = stdout_data.replace(b'\r\n', b'\n')
        self.assertEqual(expected_output, stdout_data)

if __name__ == '__main__':
    unittest.main()