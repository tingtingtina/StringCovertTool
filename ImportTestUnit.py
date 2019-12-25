# -*- coding:utf-8 -*-
from Import import ImportUtils, addParser


def main():
    importUtils = ImportUtils()
    # options = addParser()
    # importUtils.xls2xml_options(options)

    xlsPath = "E:\\stringCovertTool\\test\\App Native.xlsx"
    filePath ="E:\\stringCovertTool\\test\\values\\strings_me.xml"
    dirPath = "E:\\stringCovertTool\\test"
    importUtils.xls2xml(xlsPath, None, None, dirPath)
    # importUtils.xls2xml(xlsPath, filePath, "en", dirPath)


# 读取 xls
main()
