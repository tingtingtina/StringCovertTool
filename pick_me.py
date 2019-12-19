# -*- coding:utf-8 -*-
from Tkinter import *
import tkFileDialog
import tkMessageBox
import Xls2xml
import ErrorConstant
import os.path
from LogUtils import Log

root = Tk()
root.title("Android 字符串多语言导入导出工具")
root.geometry('300x200')  # 这里的乘是小x
# 创建一个菜单栏，这里我们可以把他理解成一个容器，在窗口的上方
menubar = Menu(root)
# 创建一个File菜单项（默认不下拉，下拉内容包括导入xml，从xml导出功能项
menu = Menu(root, tearoff=0)
# 将上面定义的空菜单命名为File，放在菜单栏中，就是装入那个容器中
menubar.add_cascade(label='功能', menu=menu)


# 在File中加入New、Open、Save等小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。
def import_func():
    tkMessageBox.showinfo("开发中", message="开发中……")

    pass


def export_func():
    window = Toplevel(root)
    window.title("导入xml")
    # 设定窗口的大小(长 * 宽)
    window.geometry('600x300')  # 这里的乘是小x

    # window.withdraw()

    isDir = False  # 导出是文件导出还是目录导出

    # 标题框
    initStartY = 60
    Label(window, text='表格路径:').place(x=10, y=initStartY)
    Label(window, text='目标文件:').place(x=10, y=initStartY + 40)
    Label(window, text='目标语言:').place(x=10, y=initStartY + 80)
    Label(window, text='目标目录:').place(x=10, y=initStartY + 120)

    # 输入框
    inputStartX = 100
    enter_width = 50  # 这个宽度可以理解成字符数呢
    enter_height = 14  # 这个宽度可以理解成字符数呢
    var_input_path = StringVar()
    edt1 = Entry(window, textvariable=var_input_path, width=enter_width).place(x=inputStartX, y=initStartY)

    var_target_file_path = StringVar()
    edt2 = Entry(window, textvariable=var_target_file_path, width=enter_width).place(x=inputStartX, y=initStartY + 40)

    var_target_lan = StringVar()
    edt3 = Entry(window, textvariable=var_target_lan, width=enter_width).place(x=inputStartX, y=initStartY + 80)

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

        xls2xmlUtils = Xls2xml.Xls2xmlUtils()
        if isDir:
            error = xls2xmlUtils.xls2xml(var1, None, None, var4)  # type: ErrorConstant.Error
        else:
            error = xls2xmlUtils.xls2xml(var1, var2, var3, None)  # type: ErrorConstant.Error

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
    Label(window, text="导出方式")
    exportFunc = [('单个文件', 0), ('目录方式', 1)]

    def callRB():
        global isDir
        isDir = (v.get() == 1)  # type: int

    # for循环创建单选框
    for text, num in exportFunc:
        Radiobutton(window, text=text, value=num, command=callRB, variable=v).pack(anchor=W)
    pass


menu.add_command(label='从 xml 导出', command=import_func)
menu.add_command(label='导入 xml', command=export_func)


# 第11步，创建菜单栏完成后，配置让菜单栏menubar显示出来
root.config(menu=menubar)
root.mainloop()  # 进入消息循环

# https://blog.csdn.net/shawpan/article/details/78759199
# https://blog.csdn.net/ahilll/article/details/81531587
# https://www.cnblogs.com/shwee/p/9427975.html
