# coding: utf-8
"""pairwise testing tool using FreeMind and PICT"""

import xml.etree.ElementTree as ET
import subprocess
import argparse
import sys
import os

class NodeType(object):
    """type of Freeminde node"""
    NO_DATA = 1
    COMMENT = 2
    VAILD_DATA = 3
    FACTOR = 4
    EXEC_OPTION = 5
    HEADER = 6
    SUB_MODEL_DEFINITIONS = 7
    CONSTRAINT_DEFINITIONS = 8
    LINK_DEF = 9
    LINK_REFER = 10
    
    @staticmethod
    def is_valid_data_node(node_type):
        return node_type == NodeType.VAILD_DATA or node_type == NodeType.LINK_REFER

class FMCTMGenerator(object):
    """generates test condition from FreeMind file"""

    def __init__(self):
        self._clsf_dict = {}
        self._pict_exec_option = ""
        self._insert_text = {}
        self._link_def = {}
    
    def _init_gendata(self):
        """initialize analysis data"""
        self._clsf_dict = {}
        self._pict_exec_option = ""
        self._insert_text = {}
        self._link_def = {}

    def get_testcon(self):
        """return last pict data"""
        return self._clsf_dict

    @staticmethod
    def _get_node_type(node):
        """get node type from node.attrib"""
        if not 'TEXT' in node.attrib:
            return NodeType.NO_DATA
        if not node.attrib['TEXT']:
            return NodeType.NO_DATA

        attrib_text = FMCTMGenerator._get_text_str(node)

        prefix_dict = {'#':NodeType.COMMENT, '<':NodeType.LINK_DEF,
                       '>':NodeType.LINK_REFER, '@':NodeType.FACTOR}
        for key, value in prefix_dict.items():
            if attrib_text[0] == key:
                return value

        word_dict = {'[pict_exec_option]':NodeType.EXEC_OPTION,
                     '[sub_model_definitions]':NodeType.SUB_MODEL_DEFINITIONS,
                     '[constraint_definitions]':NodeType.CONSTRAINT_DEFINITIONS}
        for key, value in word_dict.items():
            if key in attrib_text:
                return value

        if [x for x in node if x.attrib == {'BUILTIN': 'folder'}]:
            return NodeType.FACTOR
        return NodeType.VAILD_DATA

    @staticmethod
    def _get_text_str(node):
        return node.attrib['TEXT'].encode(sys.stdout.encoding).decode(sys.stdout.encoding)

    def _get_testcon_from_node(self, parent):
        """reads class set from freemind node"""
        node_type = self._get_node_type(parent)

        if node_type == NodeType.COMMENT:
            return self._clsf_dict

        if node_type == NodeType.EXEC_OPTION:
            for node in [y for y in list(parent) if 'TEXT' in y.attrib]:
                child_node_type = self._get_node_type(node)
                if NodeType.is_valid_data_node(child_node_type):
                    text_data = self._get_text_str(node)
                    self._pict_exec_option = self._pict_exec_option + ' ' + text_data
        
        if node_type == NodeType.HEADER or \
            node_type == NodeType.CONSTRAINT_DEFINITIONS or \
            node_type == NodeType.SUB_MODEL_DEFINITIONS:
            for node in [y for y in list(parent) if 'TEXT' in y.attrib]:
                child_node_type = self._get_node_type(node)
                if NodeType.is_valid_data_node(child_node_type):
                    text_data = self._get_text_str(node)
                    if node_type in self._insert_text:
                        print('Warning:Duplicate Insert Text[%d]' % (node_type))
                    self._insert_text[node_type] = text_data

        if node_type == NodeType.FACTOR:
            cf_text = self._get_text_str(parent)
            class_list = []
            for node in [y for y in list(parent) if 'TEXT' in y.attrib]:
                child_node_type = self._get_node_type(node)
                if NodeType.is_valid_data_node(child_node_type):
                    text_data = self._get_text_str(node)
                    class_list.append(text_data)
            if class_list:
                self._clsf_dict[cf_text] = class_list

        if node_type == NodeType.LINK_DEF:
            cf_text = self._get_text_str(parent)
            class_list = []
            for node in [y for y in list(parent) if 'TEXT' in y.attrib]:
                child_node_type = self._get_node_type(node)
                if NodeType.is_valid_data_node(child_node_type):
                    text_data = self._get_text_str(node)
                    class_list.append(text_data)
            if class_list:
                self._link_def[cf_text] = class_list

            return self._link_def

        # NodeType.NO_DATA or non type
        for node in list(parent):
            self._get_testcon_from_node(node)
        return self._clsf_dict

    def _replace_link_def(self):
        for key, value in self._clsf_dict.items():
            pass

    @staticmethod
    def _gen_pict_input_file(file_path, clsf_dict, insert_text_dict):
        try:
            with open(file_path, "w") as pict_input_file:
                for key, classlist in clsf_dict.items():
                    line = key + ':' + ",".join(classlist) + '\n'
                    pict_input_file.write(line)
                if NodeType.SUB_MODEL_DEFINITIONS in insert_text_dict:
                    pict_input_file.write(insert_text_dict[NodeType.SUB_MODEL_DEFINITIONS])
                if NodeType.CONSTRAINT_DEFINITIONS in insert_text_dict:
                    pict_input_file.write(insert_text_dict[NodeType.CONSTRAINT_DEFINITIONS])
        except IOError:
            print('Error:pict file cannot be created')

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

            self._gen_pict_input_file(file_path, self._clsf_dict, self._insert_text)

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
