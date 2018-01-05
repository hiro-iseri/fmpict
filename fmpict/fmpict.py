# coding: utf-8
"""pairwise testing tool using FreeMind and PICT
Site: https://github.com/hiro-iseri/fmpict/
License: MIT
"""

import xml.etree.ElementTree as ET
import subprocess
import argparse
import sys
import os
import codecs
import re

"""
TODO:
support pict alias
add custom option of node mark
add freemind syntax checking func
"""

class NodeType(object):
    """type of Freeminde node"""
    ETC = 0
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

class NodeMark(object):
    _INITIAL_PREFIX = {NodeType.COMMENT:'#', NodeType.LINK_DEF:'>',
                       NodeType.LINK_REFER:'<', NodeType.FACTOR:'@'}
    prefix = _INITIAL_PREFIX

    _INITIAL_MARK_WORD = {NodeType.EXEC_OPTION:'{pict_exec_option}',
                          NodeType.SUB_MODEL_DEFINITIONS:'{sub_model_definitions}',
                          NodeType.CONSTRAINT_DEFINITIONS:'{constraint_definitions}'}
    mark_word = _INITIAL_MARK_WORD

    @classmethod
    def init(cls):
        prefix = cls._INITIAL_PREFIX
        mark_word = cls._INITIAL_MARK_WORD
    
    @classmethod
    def get_node_type(cls, node_text):
        for key, value in cls.prefix.items():
            if node_text[0] == value:
                if len(node_text) == 1:
                    # empty TEXT
                    return NodeType.NO_DATA
                else:
                    return key        
        for key, value in cls.mark_word.items():
            if value in node_text:
                return key

        return NodeType.ETC


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
        """get node type by node.attrib"""
        if not 'TEXT' in node.attrib:
            return NodeType.NO_DATA
        if not node.attrib['TEXT']:
            # empty TEXT
            return NodeType.NO_DATA

        attrib_text = FMCTMGenerator._get_text_str(node)

        node_type = NodeMark.get_node_type(attrib_text)
        if node_type != NodeType.ETC:
            return node_type

        if [x for x in node if x.attrib == {'BUILTIN': 'folder'}]:
            return NodeType.FACTOR
        return NodeType.VAILD_DATA

    @staticmethod
    def _get_text_str(node):
        return node.attrib['TEXT'].encode(sys.stdout.encoding).decode(sys.stdout.encoding)

    @staticmethod
    def append_child_text_node(dict, parent):
        """add valid child node text to dict"""
        cf_text = FMCTMGenerator._get_text_str(parent)
        if cf_text[0] == NodeMark.prefix[NodeType.FACTOR]:
            cf_text = cf_text[1:]
        class_list = []
        for node in [x for x in list(parent) if 'TEXT' in x.attrib]:
            child_node_type = FMCTMGenerator._get_node_type(node)
            if NodeType.is_valid_data_node(child_node_type):
                text_data = FMCTMGenerator._get_text_str(node)
                class_list.append(text_data)
        if class_list:
            dict[cf_text] = class_list        

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
            return self._clsf_dict

        if node_type == NodeType.CONSTRAINT_DEFINITIONS or \
            node_type == NodeType.SUB_MODEL_DEFINITIONS:
            for node in [y for y in list(parent) if 'TEXT' in y.attrib]:
                child_node_type = self._get_node_type(node)
                if NodeType.is_valid_data_node(child_node_type):
                    text_data = self._get_text_str(node)
                    self._insert_text[node_type] = text_data
            return self._clsf_dict

        if node_type == NodeType.FACTOR:
            self.append_child_text_node(self._clsf_dict, parent)
            return self._clsf_dict

        if node_type == NodeType.LINK_DEF:
            self.append_child_text_node(self._link_def, parent)
            return self._clsf_dict

        # NodeType.NO_DATA or non type
        for node in list(parent):
            self._get_testcon_from_node(node)
        return self._clsf_dict

    def _replace_link_def(self):
        for key, value_list in self._clsf_dict.items():
            new_value_list = []
            for value_item in value_list:
                if value_item[0] == NodeMark.prefix[NodeType.LINK_REFER]:
                    for key_def in [keys for keys in self._link_def.keys() if value_item[1:] == keys[1:]]:
                        new_value_list.extend(self._link_def[key_def])
                else:
                    new_value_list.append(value_item)
            self._clsf_dict[key] = new_value_list

    def generate(self, input_file, only_gen_pictfile=False, save_pictfile=False, pictfile_path=""):
        """generates test condition from FreeMind file"""
        self._init_gendata()
        try:
            cls_tree = ET.parse(input_file)
        except ET.ParseError:
            Msg.p(Msg.ERR, 'cannot perse freemind file')
            raise
        except IOError:
            Msg.p(Msg.ERR, 'cannot open freemind file')
            raise

        self._get_testcon_from_node(cls_tree.getroot())
        self._replace_link_def()

        if not self._clsf_dict:
            Msg.p(Msg.ERR, 'freemind file is empty')
            return

        if pictfile_path:
            file_path = pictfile_path
        else:
            file_path = "temp.txt"

        PictRunner.gen_pict_input_file(file_path, self._clsf_dict, self._insert_text)

        if not only_gen_pictfile:
            PictRunner.print_testcondition(file_path, self._pict_exec_option)

        if not save_pictfile:
            PictRunner.delete_pict_file(file_path)

class PictRunner(object):
    @staticmethod
    def gen_pict_input_file(file_path, clsf_dict, insert_text_dict):
        try:
            with codecs.open(file_path, "w", sys.stdout.encoding) as pict_input_file:
                for key, classlist in clsf_dict.items():
                    line = key + ':' + ",".join(classlist) + '\n'
                    pict_input_file.write(line)
                if NodeType.SUB_MODEL_DEFINITIONS in insert_text_dict:
                    pict_input_file.write(insert_text_dict[NodeType.SUB_MODEL_DEFINITIONS])
                if NodeType.CONSTRAINT_DEFINITIONS in insert_text_dict:
                    pict_input_file.write(insert_text_dict[NodeType.CONSTRAINT_DEFINITIONS])
        except IOError:
            Msg.p(Msg.ERR, 'cannot create pict file')
            raise

    @staticmethod
    def print_testcondition(file_path, exec_option):
        """output class set to stdout"""
        command = "pict %s%s" % (file_path, exec_option)
        prc = subprocess.Popen(command.split())
        if prc:
            prc.wait()
        else:
            Msg.p(Msg.ERR, 'cannot run pict')
    
    @staticmethod
    def delete_pict_file(file_path):
        os.remove(file_path)

class Msg(object):
    """Manage messages to users"""
    ERR = "Error"
    WRN = "Warning"
    INF = "Info"

    @staticmethod
    def p(message_type, message):
        print('%s:%s' %(message_type, message))


def _get_parser():
    """creates FMPict parser"""
    parser = argparse.ArgumentParser(
        description='This tool generates test cases using freemind and pict')
    parser.add_argument('freemind_file_path', help='*.mm input file', type=argparse.FileType('r'))
    parser.add_argument('-p', '--pict_file_path', help='save pict file to specified path', type=str)
    parser.add_argument('-g', '--genparamlist', help='execute until pict file generation', action="store_true")
    parser.add_argument('-s', '--savepictfile', help='save pict file', action="store_true")
    return parser

def main():
    args = _get_parser().parse_args()
    gen = FMCTMGenerator()
    gen.generate(args.freemind_file_path, args.genparamlist, args.savepictfile, args.pict_file_path)

if __name__ == '__main__':
    main()
