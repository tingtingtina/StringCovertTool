#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import io
import sys

SUCCESS = 0
ERROR_DIR_NOT_EXIST = 1  # type: int #目标目录不存在
ERROR_INPUT = 2  # type: int #输入不合法
ERROR_KEY_NOT_FOUND = 3  # 没找到 key
ERROR_MODULE_NOT_FOUND = 4  # 没找到 key
EXCEPTION_EXL_FILE = 5  # 文件为空或者第一行没有内容
ERROR_EXCEL_NOT_EXIST = 6  # 文件为空或者第一行没有内容

class Error:
    desc = None  # type: str
    code = -1  # type: int

    def __init__(self, code, desc=""):
        self.desc = desc
        self.code = code

    def isError(self):
        return self.code != SUCCESS

    def get_desc(self):
        des = ""
        if self.code == SUCCESS:
            des = "导入成功！"
        elif self.code == ERROR_DIR_NOT_EXIST:
            des = "目标目录不存在"
        elif self.code == ERROR_INPUT:
            des = "输入错误，请查看以下项：\n1. 同时输入目标语言和文件，或者输入目标目录;\n2. 表格中不存在目标语言"
        elif self.code == ERROR_KEY_NOT_FOUND:
            des = "表格结构错误：\n没有检索到 key 列，key 列需命名为 Android keyName"
        elif self.code == ERROR_MODULE_NOT_FOUND:
            des = "表格结构错误：\n没有检索到 Module 列，key 列需命名为 Android module"
        elif self.code == EXCEPTION_EXL_FILE:
            des = "表格结构错误：\n表格为空或者没有检索到标题行，标题列为第一行"
        elif self.code == ERROR_EXCEL_NOT_EXIST:
            des = "请输入表格文件"
        if self.desc and des:
            self.desc = "%s\nMessage:%s" % (des, self.desc)
        elif des:
            self.desc = des
        return self.desc


class Config:
    keyTitle = "Android keyName"
    moduleTitle = "Android module"  # 内容为文件名