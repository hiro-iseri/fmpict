# coding: utf-8
"""Simple classification tree tool using FreeMind and PICT"""

import xml.etree.ElementTree as ET
import subprocess
import argparse
import sys


class FMCTMGenerator(object):
    """generates test condition from FreeMind's file"""

    def __init__(self):
        self._clsf_dict = {}

    def get_testcon(self):
        """return last class set"""
        return self._clsf_dict

    def _get_testcon_from_node(self, parent):
        """reads class set from freemind's node"""

        if not 'TEXT' in parent.attrib or not [x for x in parent if x.attrib == {'BUILTIN': 'folder'}]:
            for node in list(parent):
                self._get_testcon_from_node(node)
            return self._clsf_dict

        cf_text = parent.attrib['TEXT'].encode(sys.stdout.encoding).decode(sys.stdout.encoding)
        if not cf_text:
            if cf_text[0] != '#':
                for node in list(parent):
                    self._get_testcon_from_node(node)
            return self._clsf_dict            
        else:
            class_list = []
            for node in [y for y in list(parent) if 'TEXT' in y.attrib]:
                text_data = node.attrib['TEXT'].encode(sys.stdout.encoding).decode(sys.stdout.encoding)
                if text_data and text_data[0] != '#':
                    class_list.append(text_data)
            if class_list:
                self._clsf_dict[cf_text] = class_list

        return self._clsf_dict

    @staticmethod
    def _print_testcondition(clsf_dict):
        """output class set to stdout"""
        try:
            with open("temp.csv", "w") as pict_input_file:
                for key, classlist in clsf_dict.items():
                    line = key + ':' + ",".join(classlist) + '\n'
                    pict_input_file.write(line)
        except IOError:
            print('pict file cannot be created')
            raise
        subprocess.Popen("pict temp.csv", shell=True)

    def generate(self, input_file):
        """generates test condition from FreeMind file"""
        try:
            cls_tree = ET.parse(input_file)
        except ET.ParseError:
            print('"%s" is invalid format' % input_file)
            raise
        self._get_testcon_from_node(cls_tree.getroot())
        if not self._clsf_dict:
            print("Error:FreeMind file is invalid")
        else:
            self._print_testcondition(self._clsf_dict)

def _get_parser():
    """create parser"""
    parser = argparse.ArgumentParser(
        description='This script is test tool generates test cases from freemind.')
    parser.add_argument('freemind_file_path', help='*.mm input file', type=argparse.FileType('r'))
    parser.add_argument('-g', '--genparamlist', dest='generates param list file', help='run without calling pict')
    return parser

def main():
    parser = _get_parser()
    gen = FMCTMGenerator()
    gen.generate(parser.parse_args().freemind_file_path)

if __name__ == '__main__':
    main()
