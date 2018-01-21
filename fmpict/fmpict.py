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
    mark_icon = _INITIAL_MARK_ICON

    @classmethod
    def init(cls):
        """reset customize"""
        cls.prefix = cls._INITIAL_PREFIX
        cls.mark_word = cls._INITIAL_MARK_WORD
        cls.mark_icon = cls._INITIAL_MARK_ICON

    @staticmethod
    def is_factor(node):
        result = True
        for child in list(node):
            if NodeType.FACTOR != NodeMark.get_node_type(child):
                result = not FMCTMGenerator.is_factor(child)
            else:
                return False
        return result

    @classmethod
    def get_node_type(cls, node):
        try:
            node_text = cls.trim_tag(NodeText.get_text(node))
        except KeyError:
            return NodeType.NO_DATA

        if not node_text:
            return NodeType.NO_DATA

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

        for key, value in cls.mark_icon.items():
            if [x for x in node if x.attrib == value]:
                return key

        return NodeType.VAILD_DATA

    @classmethod
    def get_hit_tag(cls, node_text, exclude_tag_list):
        if not exclude_tag_list:
            return []

        ex_set = set(exclude_tag_list)
        tag_set = set(cls._RE_TAG_WORD.findall(node_text))
        return ex_set & tag_set

    @classmethod
    def get_tag(cls, node_text):
        return cls._RE_TAG_WORD.findall(node_text)

    @classmethod
    def trim_tag(cls, node_text):
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

class NodeText(object):
    @staticmethod
    def get_text(node):
        return node.attrib['TEXT'].encode(sys.stdout.encoding).decode(sys.stdout.encoding)

class FMCTMGenerator(object):
    """generates test condition from FreeMind file"""
    _clsf_dict = {}
    _pict_exec_option = ""
    _insert_text = {}
    _link_def = {}
    _tag_list = []
    
    @classmethod
    def _init_gendata(cls):
        """reset analysis data"""
        cls._clsf_dict = {}
        cls._pict_exec_option = ""
        cls._insert_text = {}
        cls._link_def = {}
        cls._tag_list = []

    @staticmethod
    def is_factor(node):
        result = True
        for child in list(node):
            if NodeType.FACTOR != NodeMark.get_node_type(child):
                result = FMCTMGenerator.is_factor(child)
            else:
                return False
        return result

    @classmethod
    def pickup_end_node_text(cls, parent, end_node_list):
        try:
            if len(list(parent)) == 0:
                end_node_list.append(NodeText.get_text(parent))
        except KeyError:
            return end_node_list

        for node in list(parent):
            if NodeType.is_valid_data_node(NodeMark.get_node_type(node)):
                end_node_list = cls.pickup_end_node_text(node, end_node_list)
        return end_node_list

    @classmethod
    def get_last_testconditions(cls):
        """return last pict data"""
        return cls._clsf_dict

    @staticmethod
    def _get_text_str(node):
        return NodeMark.trim_tag(NodeText.get_text(node))

    @classmethod
    def append_child_text_node(cls, out_dict, parent):
        """add valid child node text to dict"""
        end_node = []
        end_node = cls.pickup_end_node_text(parent, end_node)
        cf_text = FMCTMGenerator._get_text_str(parent)
        if cf_text[0] == NodeMark.prefix[NodeType.FACTOR]:
            cf_text = cf_text[1:]

        if end_node:
            out_dict[cf_text] = end_node

    @classmethod
    def _has_tag(cls, node):
        if not 'TEXT' in node.attrib:
            return False

        text = NodeText.get_text(node)
        return NodeMark.get_hit_tag(text, cls._tag_list)

    @classmethod
    def _get_testcon_from_node(cls, parent):
        """reads class set from freemind node"""

        node_type = NodeMark.get_node_type(parent)
        assert node_type != NodeType.COMMENT

        if node_type == NodeType.EXEC_OPTION:
            for node in [y for y in list(parent) if 'TEXT' in y.attrib]:
                child_node_type = NodeMark.get_node_type(node)
                if NodeType.is_valid_data_node(child_node_type):
                    text_data = cls._get_text_str(node)
                    cls._pict_exec_option = cls._pict_exec_option + ' ' + text_data
            return cls._clsf_dict

        if node_type == NodeType.CONSTRAINT_DEFINITIONS or \
            node_type == NodeType.SUB_MODEL_DEFINITIONS:
            for node in [y for y in list(parent) if 'TEXT' in y.attrib]:
                child_node_type = NodeMark.get_node_type(node)
                if NodeType.is_valid_data_node(child_node_type):
                    text_data = cls._get_text_str(node)
                    cls._insert_text[node_type] = text_data
            return cls._clsf_dict

        if node_type == NodeType.FACTOR:
            if cls.is_factor(parent):
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
    def get_testconditions_from_fmfile(cls, freemind_file_path, tag_list=None):
        try:
            cls_tree = ET.parse(freemind_file_path)
        except ET.ParseError:
            Msg.p(Msg.ERR, 'cannot perse freemind file')
            raise
        except IOError:
            Msg.p(Msg.ERR, 'cannot open freemind file')
            raise

        return cls.get_testconditions_from_fmet(cls_tree, tag_list)
    
    @staticmethod
    def print_fmtree(root):
        if 'TEXT' in root.attrib:
            print(root.attrib['TEXT'])
        for node in root:
            FMCTMGenerator.print_fmtree(node)
    
    @classmethod
    def preprocess_fmtree(cls, root, tag_list=None):
        for node in root:
            node_type = NodeMark.get_node_type(node) 
            if node_type == NodeType.COMMENT:
                root.remove(node)

            if 'TEXT' in node.attrib:
                if tag_list and NodeMark.get_tag(NodeText.get_text(node)):
                    if not NodeMark.get_hit_tag(NodeText.get_text(node), tag_list):
                        root.remove(node)
                if node.attrib['TEXT'] == "":
                    root.remove(node)
                node.attrib['TEXT'] = NodeMark.trim_tag(node.attrib['TEXT'])
            cls.preprocess_fmtree(node, tag_list)

    @classmethod
    def get_testconditions_from_fmet(cls, fm_tree, tag_list=None):
        cls.preprocess_fmtree(fm_tree.getroot(), tag_list)
        cls._tag_list = tag_list
        cls._get_testcon_from_node(fm_tree.getroot())
        cls._replace_link_def()
        return cls._clsf_dict

    @classmethod
    def generate(cls, input_file, only_gen_pictfile=False, save_pictfile=False, pictfile_path="", tag_list=None):
        """generates test condition from FreeMind file"""
        cls._init_gendata()

        clsf_dict = cls.get_testconditions_from_fmfile(input_file, tag_list)

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
    ERR = 3
    WRN = 2
    INF = 1
    MSG_LEVEL_DICT = {ERR:"Error", WRN:"Warning", INF:"Info"}
    msg_level = INF

    @staticmethod
    def p(message_type, message):
        if Msg.msg_level >= message_type:
            print('%s:%s'%(message_type, message))

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
        '-t', '--select_tag_list', help='select specified tag in generating', type=str)
    return parser

def get_testconditions(freemind_file_path, tag_list=""):
    return FMCTMGenerator.get_testconditions_from_fmfile(freemind_file_path,
                                                         NodeMark.get_tag_list(tag_list))

def run(freemind_file_path, genparamlist=False, savepictfile=False,pict_file_path="", tag_list=""):
    FMCTMGenerator.generate(freemind_file_path, genparamlist,
                            savepictfile, pict_file_path,
                            NodeMark.get_tag_list(tag_list))

def main():
    """execute on CUI"""
    args = _get_parser().parse_args()
    FMCTMGenerator.generate(args.freemind_file_path, args.genparamlist,
                            args.savepictfile, args.pict_file_path,
                            NodeMark.get_tag_list(args.select_tag_list))


if __name__ == '__main__':
    main()
