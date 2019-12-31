## 目的

本项目的开发目的是由于在 Android 项目中会有多语言翻译的需求，在我们做完中文给到专业人员翻译的时候，有字符串到出的需求；反之，多国语言翻译回来之后，同时有导入的需求，手动复制粘贴一定是最低效的方式。所以这个脚本只有两个功能，一个是导出，xml -> xls ，一个是导入 xls -> xml

## 使用方法

### 环境
- Python2
- python库 
    - xlrd（导入使用）
    - pyExcelerator(导出使用)

### 配置
Config 里面默认配置了 表格的 title 等属性
```python
keyTitle = "Android keyName"  # key 名（Android 字符串 name)
moduleTitle = "Android module"  # module 名（xml 文件名）
import_start_col = 2  # 从第几列开始导入
    
export_excel_name = "Output.xls"  # 导出的 excel 文件名
export_base_dir = "values-zh"  # 导出基准文件夹
export_base_title = "zh"  # 导出基准 title

export_only_zh = False  # 是否仅导出中文字符
```

## 参数说明 

### 导入

- -i 输入excel 的路径

- -f 输入目标 xml 路径

- -l 输入目标语言简写，如 en zh 等，与 ```-f``` 成对使用

- -d 输入目标文件夹，如 c:\android，文件目录结构如下（android 直接从工程中拷出即可）

  （由于默认为 en 因此文件夹支持 values-en 也支持 values）

```
├── andorid
│   ├── values-zh
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
### 导出
> 导出没有添加输入参数，直接支持可视化操作
- 单个文件，
    - 输入要导出的 excel 路径，比如，选择路径为 C:\Users\Administrator\Desktop，那么会在桌面上创建一个 Output.xls 文件，完成路径为 C:\Users\Administrator\Desktop\Output.xls
    - 输入要导出的 xml 文件，结果就会将 xml 的 键值对导出到 excel 表中
    
- 目录方式
    - 要导出的 excel 路径，同上
    - 要导出的 xml 目录路径，如 ..\android, android 目录下有如下文件格式
   
   
    ```
    ├── andorid
    │   ├── values-zh
    │   |	├── strings_device.xml
    │   |	├── strings_me.xml
    │   |	├── strings_moment.xml
    │   ├── values-de
    │   ├── values-ko
    │   ├── values
    ```
    注：目录方式会默认以 values-zh 作为基准（比如 key 的顺序），可以通过修改 Config 属性 ```export_base_dir``` 和 ```export_base_title``` 来定制
   
   ### 导出效果
   
   | Android module | Android keyName | zh   | en   | ko   |
   | -------------- | --------------- | ---- | ---- | ---- |
   | strings_me     | me_1            |      |      |      |
   | strings_me     | me_2            |      |      |      |
   | strings_me     | me_3            |      |      |      |
   | strings_moment | moment_1        |      |      |      |
   | strings_moment | moment_2        |      |      |      |
   | strings_moment | moment_3        |      |      |      |
   | strings_device | device_1        |      |      |      |
### 注意点：

- xml 目录指的都是包含着 values-zh 等目录的文件夹

- 这里的 module 指的是 同一种语言下的 strings.xml 文件的文件名

- 如果在字符串定义有数组，比如 strings-array表示，会自定义名称，比如 下面就会生成两个键值对

  - gender_item-INDEX-0:男
  - gender_item-INDEX-1:女

  ```xml
  <string-array name="gender_item">    
  	<item>男</item>    
  	<item>女</item>
  </string-array>
  ```
- 关于导入列配置 ```import_start_col```，项目使用表格 是从第 2 列开始做导入（从0开始），也就是 en 和 de 需导入，在实际使用中可根据需求处理
- ```export_only_zh``` 需求来源于，我们在项目中会追加文案（默认中文），在没有多语言翻译的时候，其他的 strings 都会写成中文，为了便于仅导出为翻译的部分，添加此字段辅助。
    - 常用使用方法， 将导出基准设为非中文的语言，如 下面将基准设为英文，并将近导出中文支付设为 true，那么导出的就是没有翻译（仅中文）的内容
    - 为什么不能将基准设为中文？ 如果以中文为基准，所有的字符串都会导出来啦
    ```python
    export_base_dir = "values"  # 导出基准文件夹
    export_base_title = "en"  # 导出基准 title
    export_only_zh = True  # 是否仅导出中文字符
    ```
## 可视化使用

- 上面直接使用参数的方式还是容易出错，建议使用下面的方式，更清晰易懂

```python pick_me.py install```

## 测试
- ImportTestUnit.py 和 ExportTestUnit.py 用户导入导出测试