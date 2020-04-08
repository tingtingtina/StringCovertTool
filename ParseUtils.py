# -*- coding: UTF-8 -*-

import xlrd
import sys
import xml.dom.minidom
import os.path

import xlwt

import Constant
from LogUtils import Log
import collections


class XLSParse:

    def __init__(self):
        # 解决中文编码问题
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def open_excel(self, filePath):
        self.data = xlrd.open_workbook(filePath)

    # 根据sheet索引获取sheet内容,sheet索引从0开始
    def sheet_by_index(self, index):
        return self.data.sheet_by_index(index)

    # 根据sheet名称获取sheet内容
    def sheet_by_name(self, name):
        return self.data.sheet_by_name(name)


class XMLParse:

    def __init__(self):
        pass

    @staticmethod
    def get_text_node_value(string_node):
        """
        :param string_node: string 结点
        :return: data 类型结点 text
        """
        if string_node.firstChild.nodeType == string_node.TEXT_NODE:
            # 获取某个元素节点的文本内容，先获取子文本节点，然后通过“data”属性获取文本内容
            if len(string_node.firstChild.data) != 0:
                value = string_node.firstChild.data
        elif string_node.firstChild.nodeType == string_node.ELEMENT_NODE:  # 元素节点
            data_node = string_node.getElementsByTagName("Data")  # 字符串样式
            if len(data_node) != 0 and len(data_node[0].firstChild.data) != 0:
                data_value = data_node[0].firstChild.data
                value = "<Data>" + data_value + "</Data>"
        return value

    @staticmethod
    def update_multi_xml_value(sub_dir_path, keys, values, modules):
        Log.info("\n\n" + sub_dir_path + "\n")
        '''
        sub_dir_path: 目标子目录，比如 value-zh
        '''
        if len(modules) == 0:
            return

        # 先排序，把 excel 中的统一 module 排到一起
        # 排序，分块处理
        current_module = modules[0]
        module_length_list = []
        current_module_len = 0
        modules_new = []
        values_new = []
        keys_new = []
        for mid, module in enumerate(modules):
            if module is None or module == "":
                continue
            if current_module != module:
                module_length_list.append(current_module_len)
                current_module = module
                current_module_len = 0

            modules_new.append(module)
            values_new.append(values[mid])
            keys_new.append(keys[mid])
            current_module_len += 1

        module_length_list.append(current_module_len)

        start = 0
        end = 0
        for module_len in module_length_list:
            end += module_len
            subKeys = keys_new[start:end]
            subValues = values_new[start:end]
            module = modules_new[start]
            start += module_len
            filePath = sub_dir_path + module + ".xml"

            XMLParse.update_xml_value(filePath, subKeys, subValues)

    @staticmethod
    def update_xml_value(file_path, keys, values):
        Log.info("--- updating xml... \n%s" % file_path)
        if not os.path.exists(file_path):
            return
        # Log.info ("--- string ---")
        # 读取文档
        xml_doc = xml.dom.minidom.parse(file_path)
        # filename
        nodes = xml_doc.getElementsByTagName('string')
        for node in nodes:
            xmlKey = node.getAttribute("name")
            xmlValue = ""  # 改变量仅用于输出
            if node.firstChild is None:
                continue
            xmlValue = XMLParse.get_text_node_value(node)

            for index, key in enumerate(keys):
                if key == xmlKey and len(values[index]) != 0:
                    node.firstChild.data = values[index]
                    Log.debug("%s : %s -- >%s " % (xmlKey, xmlValue, node.firstChild.data))
        # Log.info("--- string end ---\n")

        # 数组
        # Log.info("--- array ---")
        array_nodes = xml_doc.getElementsByTagName('string-array')
        for array_node in array_nodes:
            xmlKey = array_node.getAttribute('name')

            child_nodes = array_node.getElementsByTagName('item')
            for idx, child_node in enumerate(child_nodes):
                newKey = xmlKey + "-INDEX-" + str(idx)

                xmlValue = child_node.firstChild.data
                for index, key in enumerate(keys):
                    if key == newKey and len(values[index]) != 0:
                        child_node.firstChild.data = values[index]
                        Log.debug("%s : %s --> %s" % (newKey, xmlValue, child_node.firstChild.data))
        # Log.info("--- array end ---\n")
        writeFile = open(file_path, 'w')
        writeFile.write(xml_doc.toxml('utf-8'))
        writeFile.close()

    @staticmethod
    def get_value_and_key(file_path):
        """
        获取 xml 文件的 key - value
        :param file_path: 文件路径
        :return: dic[key]-value
        """
        if not file_path or not os.path.exists(file_path):
            Log.error("xml 文件不存在")
            return
        xml_doc = xml.dom.minidom.parse(file_path)
        nodes = xml_doc.getElementsByTagName('string')
        dic = collections.OrderedDict()
        for index, node in enumerate(nodes):
            key = node.getAttribute("name")
            if node is None or node.firstChild is None:
                continue
            value = XMLParse.get_text_node_value(node)
            if not Constant.Config.export_only_zh:
                dic[key] = value
            else:
                if is_chinese(value):
                    dic[key] = value

            # Log.info("%s : %s" % (key, value))

        array_nodes = xml_doc.getElementsByTagName("string-array")
        for array_node in array_nodes:
            key = array_node.getAttribute('name')
            child_nodes = array_node.getElementsByTagName('item')
            for idx, child_node in enumerate(child_nodes):
                newKey = key + "-INDEX-" + str(idx)
                value = XMLParse.get_text_node_value(child_node)
                if not Constant.Config.export_only_zh:
                    dic[newKey] = value
                else:
                    if is_chinese(value):
                        dic[newKey] = value
        return dic


def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False
