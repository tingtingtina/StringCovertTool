# 关于Python的编码注释# -*- coding:utf-8 -*- 详解

一.普通解释：                                                                                                                                                                                                                      如果要在python2的py文件里面写中文，则必须要添加一行声明文件编码的注释，否则python2会默认使用ASCII编码。

二.官方解释：

1. python2.1中遇到的问题：


Python 2.1 中，想要输入 Unicode 字符，只能用基于 Latin-1 的 "unicode-escape" 的方式输入 -> 对于其他非 Latin-1 的国家和用户，想要输入 Unicode 字符，就显得很繁琐，不方便。

希望是：编程人员，根据自己的喜好和需要，以任意编码方式输入字符串，都可以，这样才正常。

2. 建议选用的方案
所以，才有人给 Python 官方建议，所以才有此PEP 0263。

此建议就是：

允许在 Python 文件中，通过文件开始处的，放在注释中的，字符串形式的，声明，声明自己的 python 文件，用何种编码。

由此，需要很多地方做相应的改动，尤其是 Python 文件的解析器，可以识别此种文件编码声明。


3 具体如何声明python文件编码？
(1)如果没有此文件编码类型的声明，则 python 默认以ASCII编码去处理；如果你没声明编码，但是文件中又包含非ASCII编码的字符的话，python解析器去解析的 python 文件，自然就会报错了。

(2)必须放在python文件的第一行或第二行;

(3)支持的格式，可以有三种：

- 带等于号的：

  ```python
  coding=<encoding name>
  ```

- 最常见的，带冒号的（大多数编辑器都可以正确识别的）：

  ```python
  #!/usr/bin/python
  #-*- coding: <encoding name> -*-
  ```

- vim的：

  ```python
  #!/usr/bin/python
  vim: set fileencoding=<encoding name> :
  ```

(4)更加精确的解释是：

    符合正则表达式："^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)" 就可以;

   关于正则表达式的理解：

   1."^"表示开始；

   2."[ \t\v]"表示匹配制表符\t和垂直制表符\v，*表示匹配0次或者多次,则[ \t\v]*合起来理解就是匹配0次或者多次\t\v;

   3."#"匹配#字符，即对应标题的#字符；

   4.".*"表示接下来匹配任意字符,".*?"表示以非贪心算法匹配任意字符，对应标题中的“ -*- ”；

   5."coding"对应标题中的coding；

   6."[:=]"表示接下来的字符是":"或者"="出现的任意多个字符，对应标题中的":";

   7.[ \t]*表示接下来匹配0次或者多次\t；标题中表示使用了0次；

   8.[-_.a-zA-Z0-9]表示匹配出现'_'字符、小写字母'a至z'、大小字母'A至Z'、数字‘0至9’的任意多的字符，对应标题中的utf-8

   9.接下来标题中的" -*- "则这个官方表达式没有给出解释，因此这个正则表达式应该是不完整的，我觉得完整的正则表达式可以为：

     "^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+).*$"
————————————————
版权声明：本文为CSDN博主「xld_1992」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/xld_19920728/article/details/80534146



# optparse模块OptionParser



Python 有两个内建的模块用于处理命令行参数：
一个是 getopt，《Deep in python》一书中也有提到，只能简单处理 命令行参数；
另一个是 optparse，它功能强大，而且易于使用，可以方便地生成标准的、符合Unix/Posix 规范的命令行说明。

使用optionparser模块来解析

optionparser的执行过程：
1、导入optionparser ： from optparse import OptionParser
2、构造optionparser的对象：parser = OptionParser()
3、往optionparser对象中增加option ：parser.add_option(...),添加的内容是命令行参数，及相关的帮助信息

每个命令行参数由参数名字符串和参数属性组成，如-f或者file分别表示长短参数名：

```python
parser.add_option("-f", "--file", ...)
```

4、调用optionparser的解析函数：

```python
(options, args) = parser.parse_args()
```

5、在options中使用解析到的options，在args中使用其他的args。
options是一个字典，其key值是app_options()函数中的dest属性的参数值；value值对应的是app_options()函数中的defalut属性的参数值，或者是由命令行传入的参数

args是由positional arguments组成的列表



**add_option函数分析：**

add_option()参数说明：
- action:存储方式，分为三种store、store_false、store_truetype``:类型``  
- dest:存储的变量default:默认值
- help:帮助信息


 action的取值有那么多，我么着重说三个store、store_false、store_true 三个取值。 action默认取值store。

- store 上表示命令行参数的值保存在options对象中。例如上面一段代码，如果我们对optParser.parse_args()函数传入的参数列表中带有‘-f’，那么就会将列表中‘-f’的下一个元素作为其dest的实参filename的值，他们两个参数形成一个字典中的一个元素{filename：file_txt}。相反当我们的参数列表中没有‘-f’这个元素时，那么filename的值就会为空。

- store_false fakeArgs 中存在'-v'verbose将会返回False，而不是‘how are you’，也就是说verbose的值与'-v'的后一位无关，只与‘-v’存在不存在有关。

- store_ture 这与action="store_false"类似，只有其中有参数'-v'存在，则verbose的值为True,如果'-v'不存在，那么verbose的值为None

https://www.cnblogs.com/abella/p/10416982.html

# python中if not x:和if x is not None：和if not x is None:使用介绍

原创[努力的搬运工](https://me.csdn.net/weixin_42153985) 发布于2018-05-08 15:56:32 阅读数 8821 收藏

展开

代码中经常有三中方式判断变量是否为None，主要有三种写法:

(1) if x is None:

(2)if not x:

(3)if not x is None:

在python中None,False,空字符串，空列表，空字典，空元组都相当于False，

eg:not None

not False

not''

not()

not{}

not[]

这些都会返回True

另外，在使用列表的时候，如果你想区分开x==[]和x==None两种情况，此时使用if not x:会出现问题

eg:x=[]

y=None

x is None //False

y is None//True

not x//True

not y//True

not x is None//这里应该理解成not( x is None)所以其会返回结果True

not y is None//not (y is None) 其会返回结果False

综上：if x is not None：这种写法最清晰，且不会出错，推荐这种写法。


```

```





coercing to Unicode: need string or buffer, int found

Log.info(sheet.name + "," +sheet.nrows+","+sheet.ncols)

Log.info("name = %s， rows number = %s，clos number = %s"%(sheet.name,sheet.nrows,sheet.ncols))

UnicodeDecodeError: 'ascii' codec can't decode byte 0xef in position 2: ordinal not in range(128)

[python2（中文编码问题）：UnicodeDecodeError: 'ascii' codec can't decode byte 0x?? in position 1](https://www.cnblogs.com/walk1314/p/7251126.html)

[python中使用xlrd、xlwt操作excel表格详解](https://www.cnblogs.com/x666-6/p/8398870.html)

[Python xlrd模块读取Excel表中的数据](https://www.cnblogs.com/ilovepython/p/11068841.html)

[python里面的xlrd模块详解（一）](https://www.cnblogs.com/insane-Mr-Li/p/9092619.html)



https://www.runoob.com/python/python-basic-syntax.html





[Python中XML的读写总结](https://blog.csdn.net/hu694028833/article/details/81089959)

