# -*- coding:utf-8 -*-
from Tkinter import *
import tkFileDialog
import tkMessageBox
import Constant

import Import
from Export import ExportUtils


class TkExport:
    def __init__(self):
        pass

    @staticmethod
    def import_func(root):
        window = Toplevel(root)
        window.title("xml导出")
        # 设定窗口的大小(长 * 宽)
        window.geometry('600x300')  # 这里的乘是小x

        # 标题框
        initStartY = 60
        Label(window, text='导出表格路径:').place(x=10, y=initStartY)
        Label(window, text='xml目录:').place(x=10, y=initStartY + 40)
        # Label(window, text='基准语言目录:').place(x=10, y=initStartY + 80)
        Label(window, text='xml文件:').place(x=10, y=initStartY + 120)

        # 输入框
        inputStartX = 100
        enter_width = 50  # 这个宽度可以理解成字符数呢
        var_excel_dir_path = StringVar()
        Entry(window, textvariable=var_excel_dir_path, width=enter_width).place(x=inputStartX, y=initStartY)

        var_xml_dir_path = StringVar()
        Entry(window, textvariable=var_xml_dir_path, width=enter_width).place(x=inputStartX, y=initStartY + 40)

        # var_base_lan_dir = StringVar()
        # Entry(window, textvariable=var_base_lan_dir, width=enter_width).place(x=inputStartX, y=initStartY + 80)

        var_xml_file_path = StringVar()
        Entry(window, textvariable=var_xml_file_path, width=enter_width).place(x=inputStartX, y=initStartY + 120)

        def enter_excel_dir():
            excel_dir_path = tkFileDialog.askdirectory()
            print excel_dir_path
            var_excel_dir_path.set(excel_dir_path)

        def enter_xml_dir_path():
            xml_dir_path = tkFileDialog.askdirectory()
            print xml_dir_path
            var_xml_dir_path.set(xml_dir_path)

        def enter_xml_file_path():
            xml_file_path = tkFileDialog.askopenfilename(filetypes=[("xml file", "*.xml*")])
            print xml_file_path
            var_xml_file_path.set(xml_file_path)

        def start_convert():
            var1 = var_excel_dir_path.get()
            var2 = var_xml_dir_path.get()
            # var3 = var_base_lan_dir.get()
            var4 = var_xml_file_path.get()

            exportUtils = ExportUtils()

            isDir = callRB()  # 导出是文件导出还是目录导出

            if isDir:
                error = exportUtils.xml2xls(var1, var2)
            else:
                error = exportUtils.xml2xls_single(var1, var4)

            if error is not None:
                if error.isError():
                    tkMessageBox.showerror(title='Error', message=error.get_desc(), parent=window)
                else:
                    tkMessageBox.showinfo(title='congratulation', message=error.get_desc(), parent=window)

        # 按键
        inputStartX = 480
        Button(window, text="选择目录", command=enter_excel_dir).place(x=inputStartX, y=initStartY - 5)
        Button(window, text="选择目录", command=enter_xml_dir_path).place(x=inputStartX, y=initStartY + 35)
        Button(window, text="选择文件", command=enter_xml_file_path).place(x=inputStartX, y=initStartY + 115)
        Button(window, text="开始", command=start_convert).place(x=10, y=initStartY + 160)

        # 选择导出方式
        v = IntVar()
        # 列表中存储的是元素是元组
        Label(window, text="导出方式")
        exportFunc = [('单个文件', 0), ('目录方式', 1)]

        def callRB():
            return v.get() == 1

        # for循环创建单选框
        for text, num in exportFunc:
            Radiobutton(window, text=text, value=num, command=callRB, variable=v).pack(anchor=W)
        pass
