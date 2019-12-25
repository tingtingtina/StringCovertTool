# -*- coding:utf-8 -*-
from Tkinter import *
import tkMessageBox

from TkExport import TkExport
from TkImport import TkImport

root = Tk()
root.title("Android 字符串多语言导入导出工具")
root.geometry('300x200')  # 这里的乘是小x
# 创建一个菜单栏，这里我们可以把他理解成一个容器，在窗口的上方
menu_bar = Menu(root)
# 创建一个File菜单项（默认不下拉，下拉内容包括导入xml，从xml导出功能项
menu = Menu(root, tearoff=0)
# 将上面定义的空菜单命名为File，放在菜单栏中，就是装入那个容器中
menu_bar.add_cascade(label='功能', menu=menu)


# 在File中加入New、Open、Save等小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。
def import_func():
    # tkMessageBox.showinfo("开发中", message="开发中……")
    TkExport.import_func(root)
    pass


def export_func():
    TkImport.export_func(root)


menu.add_command(label='从 xml 导出', command=import_func)
menu.add_command(label='导入 xml', command=export_func)


# 创建菜单栏完成后，配置让菜单栏menubar显示出来
root.config(menu=menu_bar)
root.mainloop()  # 进入消息循环

# https://blog.csdn.net/shawpan/article/details/78759199
# https://www.cnblogs.com/shwee/p/9427975.html
