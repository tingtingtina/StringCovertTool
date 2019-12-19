# -*- coding:utf-8 -*-
from Tkinter import *
import tkFileDialog
import tkMessageBox
import Xls2xml
import ErrorConstant
from LogUtils import Log

window = Tk()
window.title("Android 字符串多语言导入导出工具")

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('600x300')  # 这里的乘是小x

# window.withdraw()

# 标题框
Label(window, text='表格路径:').place(x=10, y=20)
Label(window, text='目标语言:').place(x=10, y=60)
Label(window, text='目标文件:').place(x=10, y=100)
Label(window, text='目标目录:').place(x=10, y=140)

# 输入框
inputStartY = 100
enter_width = 50  # 这个宽度可以理解成字符数呢
enter_height = 14  # 这个宽度可以理解成字符数呢
var_input_path = StringVar()
Entry(window, textvariable=var_input_path, width=enter_width).place(x=inputStartY, y=20)

var_target_lan = StringVar()
Entry(window, textvariable=var_target_lan, width=enter_width).place(x=inputStartY, y=60)

var_target_file_path = StringVar()
Entry(window, textvariable=var_target_file_path, width=enter_width).place(x=inputStartY, y=100)

var_target_dir_path = StringVar()
Entry(window, textvariable=var_target_dir_path, width=enter_width).place(x=inputStartY, y=140)


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
    xls2xmlUtils = Xls2xml.Xls2xmlUtils()
    error = xls2xmlUtils.xls2xml(var_input_path.get(), None, None,
                                 var_target_dir_path.get())  # type: ErrorConstant.Error
    if error is not None:
        if error.isError():
            tkMessageBox.showerror(title='Error', message=error.get_desc(), parent=window)
        else:
            tkMessageBox.showinfo(title='congratulation', message=error.get_desc(), parent=window)


inputStartY = 480
Button(window, text="选择文件", command=enter_input_path).place(x=inputStartY, y=15)
Button(window, text="选择文件", command=enter_target_file_path).place(x=inputStartY, y=95)
Button(window, text="选择目录", command=enter_target_dir_path).place(x=inputStartY, y=135)
Button(window, text="开始", command=start_convert).place(x=10, y=140)

window.mainloop()  # 进入消息循环

# https://blog.csdn.net/shawpan/article/details/78759199
