参数说明

xls2xml

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

  