## 目的

本项目的开发目的是由于在 Android 项目中会有多语言翻译的需求，在我们做完中文给到专业人员翻译的时候，有字符串到出的需求；反之，多国语言翻译回来之后，同时有导入的需求，手动复制粘贴一定是最低效的方式。所以这个脚本只有两个功能，一个是导出，xml -> xls ，一个是导入 xls -> xml

## 使用方法

### 环境
- Python2
- python库 xlrd（导入使用）

### 配置： 
Config 里面默认配置了 表格的 title

- key 名（Android 字符串 name)：Android keyName
- module 名（xml 文件名）：Android module

## 参数说明

### 导入

### 导出

- -i 输入excel的路径

- -f 输入目标xml路径

- -l 输入目标语言简写，如 en zh 等，与 ```-f``` 成对使用

- -d 输入目标文件夹，如 c:\android，文件目录结构如下（android 直接从工程中拷出即可）

  （由于默认为 en 因此文件夹支持 values-en 也支持 values）

```
├── andorid
│   ├── value-zh
│   |	├── strings_device.xml
│   |	├── strings_me.xml
│   |	├── strings_moment.xml
│   ├── values-de
│   ├── values-ko
```

 示例，在脚本目录下执行，或在下面脚本前加路径

- 单个文件（入参有是三个 ```-i``` ```-f``` ```-l```）

```python
python xls2xml.py -i "C:\Users\Administrator\Desktop\App Native - 1126.xlsx" -l "en" -f "C:\Users\Administrator\Desktop\p\strings_moment.xml"
```

表示 从把表格中 zh 那一列内容，替换到 strings_moment.xml 文件中

- 文件夹

  ```
  python .\xls2xml.py -i "C:\Users\Administrator\Desktop\App Native - 1126.xlsx" -d "C:\Users\Administrator\Desktop\p"
  ```

## 可视化使用
- 上面直接使用参数的方式还是容易出错，建议使用下面的方式，更清晰易懂

```python pick_me.py install```