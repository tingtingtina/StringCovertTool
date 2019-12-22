# -*- coding:utf-8 -*-
from Import import ImportUtils, addParser


def main():
    importUtils = ImportUtils()
    options = addParser()
    importUtils.xls2xml_options(options)

    # xlsPath = "C:\Users\Administrator\Desktop\App Native - 1126.xlsx"
    # filePath ="C:\Users\Administrator\Desktop\p\strings_moment.xml"
    # dirPath = ""
    # importUtils.xls2xml(xlsPath, None, None, dirPath)


# 读取 xls
main()
