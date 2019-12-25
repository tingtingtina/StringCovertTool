# -*- coding:utf-8 -*-
from Tkinter import *
import tkFileDialog
import tkMessageBox
import Constant

import Import


class TkImport:
    def __init__(self):
        pass

    @staticmethod
    def export_func(root):
        window = Toplevel(root)
        window.title("导入xml")
        # 设定窗口的大小(长 * 宽)
        window.geometry('600x300')  # 这里的乘是小x

        # 标题框
        initStartY = 60
        Label(window, text='表格路径:').place(x=10, y=initStartY)
        Label(window, text='目标文件:').place(x=10, y=initStartY + 40)
        Label(window, text='目标语言:').place(x=10, y=initStartY + 80)
        Label(window, text='目标目录:').place(x=10, y=initStartY + 120)

        # 输入框
        inputStartX = 100
        enter_width = 50  # 这个宽度可以理解成字符数呢
        var_input_path = StringVar()
        Entry(window, textvariable=var_input_path, width=enter_width).place(x=inputStartX, y=initStartY)

        var_target_file_path = StringVar()
        Entry(window, textvariable=var_target_file_path, width=enter_width).place(x=inputStartX, y=initStartY + 40)

        var_target_lan = StringVar()
        Entry(window, textvariable=var_target_lan, width=enter_width).place(x=inputStartX, y=initStartY + 80)

        var_target_dir_path = StringVar()
        edt4 = Entry(window, textvariable=var_target_dir_path, width=enter_width)
        edt4.place(x=inputStartX, y=initStartY + 120)

        def enter_input_path():
            # tkMessageBox.showerror(title='Hi', message="目录异常", parent=window)
            input_path = tkFileDialog.askopenfilename(filetypes=[("excel file", "*.xls*")])
            print input_path
            var_input_path.set(input_path)

        def enter_target_file_path():
            target_file_path = tkFileDialog.askopenfilename(filetypes=[("xml file", "*.xml*")])
            print target_file_path
            var_target_file_path.set(target_file_path)

        def enter_target_dir_path():
            target_dir_path = tkFileDialog.askdirectory()
            print target_dir_path
            var_target_dir_path.set(target_dir_path)

        def start_convert():
            var1 = var_input_path.get()
            var2 = var_target_file_path.get()
            var3 = var_target_lan.get()
            var4 = var_target_dir_path.get()

            importUtils = Import.ImportUtils()

            isDir = callRB()  # 导出是文件导出还是目录导出

            if isDir:
                error = importUtils.xls2xml(var1, None, None, var4)  # type: Constant.Error
            else:
                error = importUtils.xls2xml(var1, var2, var3, None)  # type: Constant.Error

            if error is not None:
                if error.isError():
                    tkMessageBox.showerror(title='Error', message=error.get_desc(), parent=window)
                else:
                    tkMessageBox.showinfo(title='congratulation', message=error.get_desc(), parent=window)

        # 按键
        inputStartX = 480
        Button(window, text="选择文件", command=enter_input_path).place(x=inputStartX, y=initStartY - 5)
        Button(window, text="选择文件", command=enter_target_file_path).place(x=inputStartX, y=initStartY + 35)
        Button(window, text="选择目录", command=enter_target_dir_path).place(x=inputStartX, y=initStartY + 115)
        Button(window, text="开始", command=start_convert).place(x=10, y=initStartY + 160)

        # 选择导出方式
        v = IntVar()
        # 列表中存储的是元素是元组
        Label(window, text="导入方式")
        exportFunc = [('单个文件', 0), ('目录方式', 1)]

        def callRB():
            return v.get() == 1

        # for循环创建单选框
        for text, num in exportFunc:
            Radiobutton(window, text=text, value=num, command=callRB, variable=v).pack(anchor=W)
        pass
