# -*- coding:utf-8 -*-

# 1.确认目标语言
# 2.xls 中找到目标语言的 key - value(excel)
# 3.xml 中的 key - value(xml) 准备好 文件名为 moduleName
# 4.把 value(xml) 更新成 value（excel）
# 可以输出到文件或者目录（需要约定文件 values-en）

from optparse import OptionParser
from LogUtils import Log
from ParseUtils import *
import os.path
import ErrorConstant


class Xls2xmlUtils:
    keyTitle = "Android keyName"
    moduleTitle = "Android module"  # 内容为文件名
    targetLanguage = None  # 目标语言，与 filePath 成对使用
    filePath = None  # 目标文件路径
    dirPath = None  # 目标目录路径
    fromIndex = 4  # 从 fromIndex 开始往后列导入

    def __init__(self):
        pass

    def xls2xml_options(self, options):
        return self.xls2xml(options.input, options.targetFilePath, options.targetLanguage, options.targetDirPath)

    def xls2xml(self, xls_path, file_path, target_language, target_dir_path):
        """
        :param xls_path: 表格路径
        :param file_path: 目标文件路径
        :param target_language: 目标语言
        :param target_dir_path: 目标文件目录
        """
        Log.info("--- xls2xml ---")

        # 输入 excel
        xlsPath = xls_path
        self.filePath = file_path
        self.targetLanguage = target_language
        self.dirPath = target_dir_path

        # 获取 xls 对象，以及目标 sheet（这里默认为第一张表，index 从0开始）
        xlsParse = XLSParse(xlsPath)

        sheet = xlsParse.sheet_by_index(0)

        Log.info("name = %s， rows number = %s，clos number = %s" % (sheet.name, sheet.nrows, sheet.ncols))
        return self.convert(sheet)

    def covertTargetPath(self, dir_path, language):
        # type: (String, String) -> String
        """
        据目标语言拼接成真正的目标目录
        :param dir_path: 输入的目录路径 比如 C:/A
        :param language: 目标语言 zh
        :return: C:/A/values-zh 没有 values-en 则目标目录为 C:/A/values
        """

        # 如果没有 values-en 去 values找
        targetFilePath = dir_path + "\\" + "values-" + language.lower() + "\\"
        if language == "en" and not os.path.exists(targetFilePath):
            targetFilePath = dir_path + "\\" + "values"
        return targetFilePath

    def convert(self, sheet):
        """
        真正转化部分
        :param sheet: excel 的 sheet 对象
        :return: ErrorConstant.Error
        """
        Log.info("--- convert ---")
        keyIndex = -1
        moduleIndex = -1
        tempLanguageIndex = -1
        # 返回由该行中所有单元格的数据组成的列表
        try:
            firstRow = sheet.row_values(0)
        except Exception as e:
            return ErrorConstant.Error(ErrorConstant.EXCEPTION_EXL_FILE, e.message)

        if len(firstRow) == 0:
            return ErrorConstant.Error(ErrorConstant.ERROR_KEY_NOT_FOUND)

        for index in range(len(firstRow)):
            if firstRow[index] == self.keyTitle:
                keyIndex = index
                pass
            elif firstRow[index] == self.moduleTitle:
                moduleIndex = index
                pass
            elif firstRow[index] == self.targetLanguage:
                tempLanguageIndex = index
                pass

        if keyIndex == -1:
            return ErrorConstant.Error(ErrorConstant.ERROR_KEY_NOT_FOUND)

        # 获取 key 集合，并删除 title 项
        xmlKeys = sheet.col_values(keyIndex)
        del xmlKeys[0]

        if self.filePath is not None and self.targetLanguage is not None:  # 输入是文件，指定目标语言
            Log.debug("keyIndex = %s moduleIndex = %s languageIndex = %s" % (keyIndex, moduleIndex, tempLanguageIndex))
            # 获取 value 集合，并删除 title 项
            xmlValues = sheet.col_values(tempLanguageIndex)
            del xmlValues[0]

            XMLParse.update_xml_value(self.filePath, xmlKeys, xmlValues)
            return ErrorConstant.Error(ErrorConstant.SUCCESS)

        Log.debug("Not file")

        xmlModules = sheet.col_values(moduleIndex)
        del xmlModules[0]

        if moduleIndex == -1:
            return ErrorConstant.Error(ErrorConstant.ERROR_MODULE_NOT_FOUND)

        if self.dirPath is None or len(self.dirPath) == 0:  # 目录为空，返回
            Log.error("Error：输入不合法")
            return ErrorConstant.Error(ErrorConstant.ERROR_INPUT)

        if not os.path.exists(self.dirPath):
            Log.error("Error：目标目录不存在 %s" % self.dirPath)
            return ErrorConstant.Error(ErrorConstant.ERROR_DIR_NOT_EXIST)

        for index, title in enumerate(firstRow):
            if index < self.fromIndex:
                continue
            languageIndex = index
            targetLanguage = title
            # print languageIndex
            # print title
            xmlValues = sheet.col_values(languageIndex)
            del xmlValues[0]
            # 文件路径（子目录） 比如; value-zh
            # ├── android
            # │   ├── values-zh
            # │   |	├── strings_device.xml
            # │   |	├── strings_me.xml
            # │   |	├── strings_moment.xml
            # │   ├── values-de
            # │   ├── values-ko
            sub_dir_path = self.covertTargetPath(self.dirPath, targetLanguage)
            if os.path.exists(sub_dir_path):
                XMLParse.update_mutixml_value(sub_dir_path, xmlKeys, xmlValues, xmlModules)

        return ErrorConstant.Error(ErrorConstant.SUCCESS)


def addParser():
    parser = OptionParser()
    parser.add_option("-i", "--input", help="excel file path")
    parser.add_option("-f", "--targetFilePath", help="means target output is xml file and input the file path")
    parser.add_option("-l", "--targetLanguage", help="target language shortname(just for output is file)")
    parser.add_option("-d", "--targetDirPath", help="means target output is dir contains xml file(s)")

    (options, args) = parser.parse_args()
    Log.info("options: %s, args: %s" % (options, args))
    return options


# def main():
#     xls2xmlUtils = Xls2xmlUtils()
#     options = addParser()
#     xlsPath = "C:\Users\Administrator\Desktop\App Native - 1126.xlsx"
#     # filePath ="C:\Users\Administrator\Desktop\p\strings_moment.xml"
#     dirPath = "E:\Ninebot-liting\stringCovertTool"
#
#     # xls2xmlUtils.xls2xml_options(options)
#     xls2xmlUtils.xls2xml(xlsPath, None, None, dirPath)
#     Log.info("Done!")
#
#
# # 读取 xls
# main()
