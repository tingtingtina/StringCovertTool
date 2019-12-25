# -*- coding:utf-8 -*-
from Export import ExportUtils


def main():
    exportUtils = ExportUtils()

    xls_dir = "E:\\stringCovertTool\\test"
    input_dir = "E:\\stringCovertTool\\test"
    file_path = "E:\\stringCovertTool\\test\\strings_me.xml"
    # exportUtils.xml2xls(xls_dir, input_dir)
    exportUtils.xml2xls_single(xls_dir, file_path)


# 读取 xls
main()
