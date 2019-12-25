# -*- coding:utf-8 -*-
import re

import Constant
from ParseUtils import *
import pyExcelerator


# 单个文件：获取文件 key - value 分别存放在 excel表格指定列


class ExportUtils:

    def __init__(self):
        pass

    def xml2xls(self, xls_dir, input_dir):
        # type: (str, str) -> Constant.Error
        if not xls_dir or not os.path.exists(xls_dir):
            return Constant.Error(Constant.ERROR_DIR_NOT_EXIST, "excel dir")
        if not input_dir or not os.path.exists(input_dir):
            return Constant.Error(Constant.ERROR_DIR_NOT_EXIST, "xml dir")

        xlsPath = os.path.join(xls_dir, Constant.Config.export_excel_name)
        workbook = pyExcelerator.Workbook()
        ws = workbook.add_sheet('Sheet1')
        # row col content
        ws.write(0, 0, Constant.Config.moduleTitle)
        ws.write(0, 1, Constant.Config.keyTitle)
        ws.write(0, 2, Constant.Config.export_base_title)

        # 获取某个文件夹的所有文件，作为标准 这里是 value-zh
        base_dir = os.path.join(input_dir, Constant.Config.export_base_dir)
        #  os.walk(path)返回三个值：
        #  parent, 表示path的路径、
        #  dirnames, path路径下的文件夹的名字
        #  filenames path路径下文件夹以外的其他文件。
        print input_dir
        sub_dir_names = []
        for _, dir_names, _ in os.walk(input_dir):
            if dir_names:
                sub_dir_names = dir_names
                break
        print sub_dir_names

        row = 1
        # 文件夹下所有文件
        files = os.listdir(base_dir)
        for filename in files:
            module_name = getModuleName(filename)
            if not module_name:
                continue
            file_path = os.path.join(base_dir, filename)  # 文件路径
            base_dict = XMLParse.get_value_and_key(file_path)

            col = 3  # base_dic 占用 0 和 1 2
            for dir_name in sub_dir_names:
                cur_dir_path = os.path.join(input_dir, dir_name)
                if cur_dir_path == base_dir:
                    continue  # 标准文件夹不处理

                # 当前文件夹的语言
                lan = getDirLan(input_dir, cur_dir_path)
                print lan
                if not lan:  # 文件夹爱不符合规范不处理（values-lan 或 values）
                    continue

                # 获取其他按文件夹下的该文件路径
                cur_file = os.path.join(cur_dir_path, filename)
                if not os.path.exists(cur_file):
                    # 路径不存在，不处理，跳过
                    continue

                # 写标题
                ws.write(0, col, lan)
                cur_dict = XMLParse.get_value_and_key(cur_file)
                (base_dict, cur_dict) = sortDic(base_dict, cur_dict)
                writeDict(ws, cur_dict, row, col, None, False)  # 仅写 value
                col += 1  # 写完非标准文件的内容，坐标右移（列+1）

            # 最后写 标准文件的 key（0）-values（1）
            writeDict(ws, base_dict, row, 0, module_name, True)

            row = len(base_dict)
            print("row = %s" % row)

        workbook.save(xlsPath)
        return Constant.Error(Constant.SUCCESS)

    def xml2xls_single(self, xls_dir, input_file_path):
        # type: (str, str) -> object
        if not xls_dir or not os.path.exists(xls_dir):
            return Constant.Error(Constant.ERROR_DIR_NOT_EXIST, "excel dir")
        if not input_file_path or not os.path.exists(input_file_path):
            return Constant.Error(Constant.ERROR_XML_FILE_NOT_EXIST)
        xlsPath = os.path.join(xls_dir, Constant.Config.export_excel_name)
        workbook = pyExcelerator.Workbook()
        ws = workbook.add_sheet('Sheet1')
        # row col content
        ws.write(0, 0, Constant.Config.keyTitle)
        dic = XMLParse.get_value_and_key(input_file_path)
        writeDict(ws, dic, 1, 0, None, True)
        workbook.save(xlsPath)
        return Constant.Error(Constant.SUCCESS)


def getModuleName(xml_file_name):
    m = re.search('(.*?).xml', xml_file_name)
    module_name = ''
    if m:
        module_name = m.group(1)
        # print module_name
    return module_name


def getDirLan(input_dir, dir_path):
    """
    子文件夹为 values 时默认为 en
    :param input_dir: 目标文件夹（包含这 values等文件夹的路径）
    :param dir_path: 子文件夹路径 一般 是 path/values-zh 等
    :return str 文件夹表示的语言 比如 values-zh 语言为 zh
    """
    lan = ""
    if dir_path == os.path.join(input_dir, "values"):
        lan = "en"
    else:
        dirSplit = dir_path.split('values-')
        if len(dirSplit) > 1:
            lan = dirSplit[1]
        else:
            # cur_dir_path 文件夹不符合规则
            pass
    return lan


def writeDict(ws, dic, start_row, col, module, isKeepKey):
    row = start_row
    for (key, value) in dic.items():
        Log.info("%s : %s" % (key, value))
        if isKeepKey:
            if module:
                ws.write(row, col, module)
                ws.write(row, col + 1, key)
                ws.write(row, col + 2, value)
            else:
                ws.write(row, col, key)
                ws.write(row, col + 1, value)
        else:
            ws.write(row, col, value)
        row += 1


def sortDic(dict1, dict2):
    """
    dic2 根据 dict1 key 的顺序排序，如果 dict2 中的key不在 dict1中存在，则添加至 dict1最后
    :param dict1: 目标 key 顺序
    :param dict2:
    :return:
    """
    result_dict = collections.OrderedDict()
    for (key, value) in dict1.items():
        isMatch = False
        for (temp_key, temp_value) in dict2.items():
            if key == temp_key:
                isMatch = True
                result_dict[key] = temp_value
                del dict2[key]
        if not isMatch:  # 循环结束，没有找到
            result_dict[key] = ""
        isMatch = False
    if len(dict2) != 0:
        for (key, value) in dict2.items():
            result_dict[key] = value
            dict1[key] = ""
    return dict1, result_dict
