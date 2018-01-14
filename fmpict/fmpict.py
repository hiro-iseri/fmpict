# coding: utf-8
"""testing tool using FreeMind and PICT
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

"""coding policy:
- support both python 2.7 and python 3
- depend on only standard libraries
"""

class NodeType(object):
    """type of FreeMind node"""
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
        """check value(or class)"""
        return node_type == NodeType.VAILD_DATA or node_type == NodeType.LINK_REFER

class NodeMark(object):
    """providing identification capabilities for node type"""
    _INITIAL_PREFIX = {NodeType.COMMENT:'#', NodeType.LINK_DEF:'>',
                       NodeType.LINK_REFER:'<', NodeType.FACTOR:'@'}
    prefix = _INITIAL_PREFIX

    _INITIAL_MARK_WORD = {NodeType.EXEC_OPTION:'{pict_exec_option}',
                          NodeType.SUB_MODEL_DEFINITIONS:'{sub_model_definitions}',
                          NodeType.CONSTRAINT_DEFINITIONS:'{constraint_definitions}'}
    mark_word = _INITIAL_MARK_WORD
    _RE_TAG_WORD = re.compile(r"\[[\w_\-]+\]")
    
    _INITIAL_MARK_ICON = {NodeType.FACTOR:{'BUILTIN': 'folder'}}

    @classmethod
    def init(cls):
        """reset customize"""
        cls.prefix = cls._INITIAL_PREFIX
        cls.mark_word = cls._INITIAL_MARK_WORD
    
    @classmethod
    def get_node_type_from_text(cls, node_text):
        if not node_text:
            return NodeType.ETC
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

    @classmethod
    def get_node_type_from_icon(cls, node):
        if [x for x in node if x.attrib == {'BUILTIN': 'folder'}]:
            return NodeType.FACTOR
        return NodeType.ETC

    @classmethod
    def get_excluding_tag(cls, node_text, exclude_tag_list):
        if not exclude_tag_list:
            return []

        ex_set = set(exclude_tag_list)
        tag_set = set(cls._RE_TAG_WORD.findall(node_text))
        return ex_set & tag_set

    @classmethod
    def get_text_excluding_tag(cls, node_text):
        if not node_text:
            return node_text

        text = node_text
        tag_set = set(cls._RE_TAG_WORD.findall(node_text))
        for tag in tag_set:
            text = text.replace(tag, "")
        return text 

    @classmethod
    def get_tag_list(cls, option_text):
        if not option_text:
            return None
        return cls._RE_TAG_WORD.findall(option_text)

class FMCTMGenerator(object):
    """generates test condition from FreeMind file"""
    _clsf_dict = {}
    _pict_exec_option = ""
    _insert_text = {}
    _link_def = {}
    _exclude_tag_list = []
    
    @classmethod
    def _init_gendata(cls):
        """reset analysis data"""
        cls._clsf_dict = {}
        cls._pict_exec_option = ""
        cls._insert_text = {}
        cls._link_def = {}
        cls._exclude_tag_list = []

    @classmethod
    def get_last_testconditions(cls):
        """return last pict data"""
        return cls._clsf_dict

    @staticmethod
    def _get_node_type(node):
        """get node type by node.attrib"""
        if not 'TEXT' in node.attrib:
            return NodeType.NO_DATA
        if not node.attrib['TEXT']:
            # empty TEXT
            return NodeType.NO_DATA

        attrib_text = FMCTMGenerator._get_text_str(node)

        node_type = NodeMark.get_node_type_from_text(attrib_text)
        if node_type != NodeType.ETC:
            return node_type

        node_type = NodeMark.get_node_type_from_icon(node)
        if node_type != NodeType.ETC:
            return node_type

        return NodeType.VAILD_DATA

    @staticmethod
    def _get_raw_text_str(node):
        return node.attrib['TEXT'].encode(sys.stdout.encoding).decode(sys.stdout.encoding)

    @staticmethod
    def _get_text_str(node):
        text = FMCTMGenerator._get_raw_text_str(node)
        return NodeMark.get_text_excluding_tag(text)

    @staticmethod
    def append_child_text_node(out_dict, parent):
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
            out_dict[cf_text] = class_list

    @classmethod
    def _has_tag(cls, node):
        if not 'TEXT' in node.attrib:
            return False

        text = FMCTMGenerator._get_raw_text_str(node)
        return NodeMark.get_excluding_tag(text, cls._exclude_tag_list)

    @classmethod
    def _get_testcon_from_node(cls, parent):
        """reads class set from freemind node"""
        node_type = cls._get_node_type(parent)

        if node_type == NodeType.COMMENT:
            return cls._clsf_dict

        if cls._has_tag(parent):
            return cls._clsf_dict            

        if node_type == NodeType.EXEC_OPTION:
            for node in [y for y in list(parent) if 'TEXT' in y.attrib]:
                child_node_type = cls._get_node_type(node)
                if NodeType.is_valid_data_node(child_node_type):
                    text_data = cls._get_text_str(node)
                    cls._pict_exec_option = cls._pict_exec_option + ' ' + text_data
            return cls._clsf_dict

        if node_type == NodeType.CONSTRAINT_DEFINITIONS or \
            node_type == NodeType.SUB_MODEL_DEFINITIONS:
            for node in [y for y in list(parent) if 'TEXT' in y.attrib]:
                child_node_type = cls._get_node_type(node)
                if NodeType.is_valid_data_node(child_node_type):
                    text_data = cls._get_text_str(node)
                    cls._insert_text[node_type] = text_data
            return cls._clsf_dict

        if node_type == NodeType.FACTOR:
            cls.append_child_text_node(cls._clsf_dict, parent)
            return cls._clsf_dict

        if node_type == NodeType.LINK_DEF:
            cls.append_child_text_node(cls._link_def, parent)
            return cls._clsf_dict

        # NodeType.NO_DATA or non type
        for node in list(parent):
            cls._get_testcon_from_node(node)
        return cls._clsf_dict

    @classmethod
    def _replace_link_def(cls):
        for key, value_list in cls._clsf_dict.items():
            new_value_list = []
            for value_item in value_list:
                if value_item[0] == NodeMark.prefix[NodeType.LINK_REFER]:
                    for key_def in [keys for keys in cls._link_def.keys() if value_item[1:] == keys[1:]]:
                        new_value_list.extend(cls._link_def[key_def])
                else:
                    new_value_list.append(value_item)
            cls._clsf_dict[key] = new_value_list

    @classmethod
    def get_testconditions_from_fmfile(cls, freemind_file_path, exclude_tag_list):
        try:
            cls_tree = ET.parse(freemind_file_path)
        except ET.ParseError:
            Msg.p(Msg.ERR, 'cannot perse freemind file')
            raise
        except IOError:
            Msg.p(Msg.ERR, 'cannot open freemind file')
            raise

        return cls.get_testconditions_from_fmet(cls_tree, exclude_tag_list)
    
    @classmethod
    def get_testconditions_from_fmet(cls, fm_tree, exclude_tag_list=None):
        cls._exclude_tag_list = exclude_tag_list
        cls._get_testcon_from_node(fm_tree.getroot())
        cls._replace_link_def()
        return cls._clsf_dict

    @classmethod
    def generate(cls, input_file, only_gen_pictfile=False, save_pictfile=False, pictfile_path="", exclude_tag_list=None):
        """generates test condition from FreeMind file"""

        cls._init_gendata()

        clsf_dict = cls.get_testconditions_from_fmfile(input_file, exclude_tag_list)

        if not clsf_dict:
            Msg.p(Msg.ERR, 'freemind file is empty')
            return

        if pictfile_path:
            file_path = pictfile_path
        else:
            file_path = PictRunner.DEFAULT_INPUT_FILE_PATH

        PictRunner.gen_pict_input_file(file_path, clsf_dict, cls._insert_text)

        if not only_gen_pictfile:
            PictRunner.print_testcondition(file_path, cls._pict_exec_option)

        if not save_pictfile:
            PictRunner.delete_pict_file(file_path)

class PictRunner(object):
    DEFAULT_INPUT_FILE_PATH = "temp.txt"

    @staticmethod
    def gen_pict_input_file(file_path, clsf_dict, insert_text_dict):
        """generate pict input file"""

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
    """managing message for users"""
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
    parser.add_argument(
        '-g', '--genparamlist', help='execute until pict file generation', action="store_true")
    parser.add_argument('-s', '--savepictfile', help='save pict file', action="store_true")
    parser.add_argument(
        '-e', '--exclude_tag_list', help='exclude specified tag in generating', type=str)
    return parser

def get_testconditions(freemind_file_path, exclude_tag_list=""):
    FMCTMGenerator.get_testconditions_from_fmfile(freemind_file_path,
                                                  NodeMark.get_tag_list(exclude_tag_list))

def run(freemind_file_path, genparamlist=False, savepictfile=False,pict_file_path="", taglist=""):
    FMCTMGenerator.generate(freemind_file_path, genparamlist,
                            savepictfile, pict_file_path,
                            NodeMark.get_tag_list(taglist))

def main():
    """execute on CUI"""
    args = _get_parser().parse_args()
    FMCTMGenerator.generate(args.freemind_file_path, args.genparamlist,
                            args.savepictfile, args.pict_file_path,
                            NodeMark.get_tag_list(args.exclude_tag_list))

if __name__ == '__main__':
    main()
