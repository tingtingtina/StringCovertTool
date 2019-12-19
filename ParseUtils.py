# -*- coding: UTF-8 -*-

import xlrd
import sys
import xml.dom.minidom
import os.path
from LogUtils import Log


class XLSParse:

    def __init__(self, filePath):
        # 解决中文编码问题
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.data = xlrd.open_workbook(filePath)

    # 根据sheet索引获取sheet内容,sheet索引从0开始
    def sheet_by_index(self, index):
        return self.data.sheet_by_index(index)

    # 根据sheet名称获取sheet内容
    def sheet_by_name(self, name):
        return self.data.sheet_by_name(name)


class XMLParse:
    @staticmethod
    def update_mutixml_value(sub_dir_path, keys, values, modules):
        Log.info("\n\n" + sub_dir_path + "\n\n")
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
        for mid, module in enumerate(modules):
            if module is None or module == "":
                del modules[mid]
                del keys[mid]
                del values[mid]
                continue
            if current_module != module:
                module_length_list.append(current_module_len)
                current_module = module
                current_module_len = 0

            current_module_len += 1

        module_length_list.append(current_module_len)

        start = 0
        end = 0
        for module_len in module_length_list:
            end += module_len
            subKeys = keys[start:end]
            subValues = values[start:end]
            module = modules[start]
            start += module_len
            filePath = sub_dir_path + module + ".xml"

            XMLParse.update_xml_value(filePath, subKeys, subValues)

    @staticmethod
    def update_xml_value(filepath, keys, values):
        # Log.info("--- updating xml... --- %s"%filepath)
        if not os.path.exists(filepath):
            return
        # Log.info ("--- string ---")
        # 读取文档
        xmldoc = xml.dom.minidom.parse(filepath)
        # filename
        nodes = xmldoc.getElementsByTagName('string')
        for node in nodes:
            xmlKey = node.getAttribute("name")
            xmlValue = ""  # 改变量仅用于输出
            if node.firstChild is None:
                continue
            if node.firstChild.nodeType == node.TEXT_NODE:
                # 获取某个元素节点的文本内容，先获取子文本节点，然后通过“data”属性获取文本内容
                if len(node.firstChild.data) != 0:
                    xmlValue = node.firstChild.data
                else:
                    continue
            elif node.firstChild.nodeType == node.ELEMENT_NODE:  # 元素节点
                data_node = node.getElementsByTagName("Data")  # 字符串样式
                if len(data_node) != 0 and len(data_node[0].firstChild.data) != 0:
                    data_value = data_node[0].firstChild.data
                    xmlValue = "<Data>" + data_value + "</Data>"
                else:
                    continue

            for index, key in enumerate(keys):
                if key == xmlKey and len(values[index]) != 0:
                    node.firstChild.data = values[index]
                    Log.info("%s : %s -- >%s " % (xmlKey, xmlValue, node.firstChild.data))
        # Log.info("--- string end ---\n")

        # 数组
        # Log.info("--- array ---")
        array_nodes = xmldoc.getElementsByTagName('string-array')
        for array_node in array_nodes:
            xmlKey = array_node.getAttribute('name')

            child_nodes = array_node.getElementsByTagName('item')
            for idx, child_node in enumerate(child_nodes):
                newKey = xmlKey + "-INDEX-" + str(idx)

                xmlValue = child_node.firstChild.data
                for index, key in enumerate(keys):
                    if key == newKey and len(values[index]) != 0:
                        child_node.firstChild.data = values[index]
                        Log.info("%s : %s --> %s" % (newKey, xmlValue, child_node.firstChild.data))
        # Log.info("--- array end ---\n")
        writeFile = open(filepath, 'w')
        writeFile.write(xmldoc.toxml('utf-8'))
        writeFile.close()
