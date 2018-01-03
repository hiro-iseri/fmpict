# coding: utf-8
"""Simple classification tree tool using FreeMind and PICT"""

import xml.etree.ElementTree as ET
import subprocess
import argparse
import sys
import os

class NodeType(object):
    NO_DATA = 1
    COMMENT = 2
    VAILD_DATA = 3
    FACTOR = 4
    EXEC_OPTION = 5

class FMCTMGenerator(object):
    """generates test condition from FreeMind's file"""

    def __init__(self):
        self._clsf_dict = {}
        self._pict_exec_option = ""
    
    def _init_gendata(self):
        self._clsf_dict = {}
        self._pict_exec_option = ""

    def get_testcon(self):
        """return last class set"""
        return self._clsf_dict

    @staticmethod
    def _get_node_type(node):
        if not 'TEXT' in node.attrib:
            return NodeType.NO_DATA
        if not node.attrib['TEXT']:
            return NodeType.NO_DATA
        attrib_text = node.attrib['TEXT'].encode(sys.stdout.encoding).decode(sys.stdout.encoding)
        if attrib_text[0] == '#':
            return NodeType.COMMENT
        if '[pict_exec_option]' in attrib_text:
            return NodeType.EXEC_OPTION
        if [x for x in node if x.attrib == {'BUILTIN': 'folder'}]:
            return NodeType.FACTOR
        return NodeType.VAILD_DATA

    def _get_testcon_from_node(self, parent):
        """reads class set from freemind's node"""
        node_type = self._get_node_type(parent)

        if node_type == NodeType.NO_DATA:
            for node in list(parent):
                self._get_testcon_from_node(node)
            return self._clsf_dict

        if node_type == NodeType.COMMENT:
            return self._clsf_dict

        if node_type == NodeType.EXEC_OPTION:
            for node in [y for y in list(parent) if 'TEXT' in y.attrib]:
                child_node_type = self._get_node_type(node)
                if child_node_type == NodeType.VAILD_DATA:
                    text_data = node.attrib['TEXT'].encode(sys.stdout.encoding).decode(sys.stdout.encoding)
                    self._pict_exec_option = self._pict_exec_option + ' ' + text_data
        
        if node_type == NodeType.FACTOR:
            cf_text = parent.attrib['TEXT'].encode(sys.stdout.encoding).decode(sys.stdout.encoding)
            class_list = []
            for node in [y for y in list(parent) if 'TEXT' in y.attrib]:
                child_node_type = self._get_node_type(node)
                if child_node_type == NodeType.VAILD_DATA:
                    text_data = node.attrib['TEXT'].encode(sys.stdout.encoding).decode(sys.stdout.encoding)
                    class_list.append(text_data)
            if class_list:
                self._clsf_dict[cf_text] = class_list

            return self._clsf_dict

        for node in list(parent):
            self._get_testcon_from_node(node)
        return self._clsf_dict

    @staticmethod
    def _gen_pict_input_file(file_path, clsf_dict):
        try:
            with open(file_path, "w") as pict_input_file:
                for key, classlist in clsf_dict.items():
                    line = key + ':' + ",".join(classlist) + '\n'
                    pict_input_file.write(line)
        except IOError:
            print('Error:pict file cannot be created')
            raise

    @staticmethod
    def _print_testcondition(file_path, exec_option):
        """output class set to stdout"""
        command = "pict %s%s" % (file_path, exec_option)
        prc = subprocess.Popen(command.split())
        if prc:
            prc.wait()
        else:
            print('Error:cannot run pict')

    def generate(self, input_file, only_gen_pictfile=False, save_pictfile=False, pictfile_path=""):
        """generates test condition from FreeMind file"""

        self._init_gendata()
        try:
            cls_tree = ET.parse(input_file)
        except ET.ParseError:
            print('"%s" is invalid format' % input_file)
            raise
        self._get_testcon_from_node(cls_tree.getroot())
        if not self._clsf_dict:
            print("Error:FreeMind file is invalid")
        else:
            if pictfile_path:
                file_path = pictfile_path
            else:
                file_path = "temp.csv"
            self._gen_pict_input_file(file_path, self._clsf_dict)
            if not only_gen_pictfile:
                self._print_testcondition(file_path, self._pict_exec_option)
            if not save_pictfile:
                os.remove(file_path)

def _get_parser():
    """create parser"""
    parser = argparse.ArgumentParser(
        description='This script is test tool generates test cases from freemind.')
    parser.add_argument('freemind_file_path', help='*.mm input file', type=argparse.FileType('r'))
    parser.add_argument('-p', '--pict_file_path', help='pict file path', type=str)
    parser.add_argument('-g', '--genparamlist', help='run without calling pict', action="store_true")
    parser.add_argument('-s', '--savepictfile', help='save pict file', action="store_true")
    return parser

def main():
    args = _get_parser().parse_args()
    gen = FMCTMGenerator()
    gen.generate(args.freemind_file_path, args.genparamlist, args.savepictfile, args.pict_file_path)

if __name__ == '__main__':
    main()
