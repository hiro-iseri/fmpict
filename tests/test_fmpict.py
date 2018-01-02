# coding: utf-8

import unittest
import sys
import os
import subprocess

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(root_path)
sys.path.insert(0, root_path)
import fmpict

class TestFMPict(unittest.TestCase):
    def test_hoge(self):
        self.assertEqual(True, True)
        command = r'python %s\fmpict\fmpict.py %s' % (root_path, root_path + r'\tests\fm_sample\simple.mm')
        print(command)
        out_proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print("***outout***")
        print(out_proc.stdout.read())
#        subprocess.Popen(r"python %s\\fmpict\\fmpict.py >%soutput.txt" % (root_path, root_path + '\\tests\\'), shell=True)

if __name__ == '__main__':
    unittest.main()