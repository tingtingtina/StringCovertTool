# -*- coding:utf-8 -*-

# 1.确认目标语言
# 2.xls 中找到目标语言的 key - value(excel)
# 3.xml 中的 key - value(xml) 准备好 文件名为 moduleName
# 4.把 value(xml) 更新成 value（excel）
# 可以输出到文件或者目录（需要约定文件 values-en）

from optparse import OptionParser
from LogUtils import Log
from ParseUtils import XLSParse
from ParseUtils import XMLParse
import os.path

keyTitle = "Android keyName"
moduleTitle = "Android module" #内容为文件名
targetLanguage = None #目标语言，与 filePath 成对使用
filePath = None # 目标文件路径
# filePath ="C:\Users\Administrator\Desktop\p\strings_moment.xml"
dirPath = None # 目标目录路径
# dirPath = "C:\Users\Administrator\Desktop\p" 

xmlKeys = [] # 表格的 key
xmlValues = []
fromIndex = 4 # 从 fromIndex 开始往后列导入

def addParser():
    parser = OptionParser()
    parser.add_option("-i","--input", help="excel file path")
    parser.add_option("-f","--targetFilePath", help="means target output is xml file and input the file path")
    parser.add_option("-l", "--targetLanguage", help="target language shortname(just for output is file)")
    parser.add_option("-d","--targetDirPath", help="means target output is dir contains xml file(s)")

    (options, args) = parser.parse_args()
    Log.info("options: %s, args: %s" % (options, args))
    return options
    
def xls2xml(options):
    Log.info("--- xls2xml ---")
    global targetLanguage
    global filePath
    global dirPath

    # 输入 excel
    # xlsPath ="C:\Users\Administrator\Desktop\App Native - 1126.xlsx"
    xlsPath = options.input
    filePath = options.targetFilePath
    targetLanguage = options.targetLanguage
    dirPath = options.targetDirPath

    # 获取 xls 对象，以及目标 sheet（这里默认为第一张表，index 从0开始）
    xlsParse = XLSParse(xlsPath)
    sheet = xlsParse.sheet_by_index(0)
    Log.info("name = %s， rows number = %s，clos number = %s"%(sheet.name,sheet.nrows,sheet.ncols))
    convert(sheet)
   
def covertTargetPath(dirPath, language):
    # 如果没有 values-en 去 values找
    targetFilePath = dirPath + "\\"+"values-"+ language.lower() + "\\"
    if language == "en" and not os.path.exists(targetFilePath):
        targetFilePath = dirPath + "\\"+"values"
    return targetFilePath

def convert(sheet):
    global targetLanguage
    Log.info("--- convert ---")
    languageIndex = tempLanguageIndex = -1
     #返回由该行中所有单元格的数据组成的列表
    fristRow = sheet.row_values(0)
    for index in range(len(fristRow)):
        if fristRow[index] == keyTitle:
            keyIndex = index
            pass
        elif fristRow[index] == moduleTitle:
            moduleIndex = index
            pass
        elif fristRow[index] == targetLanguage:
            tempLanguageIndex = index
            pass
  

    # 获取 key 集合，并删除 title 项
    xmlKeys = sheet.col_values(keyIndex)
    del xmlKeys[0]

    xmlModules = sheet.col_values(moduleIndex)
    del xmlModules[0]

    if filePath is not None and targetLanguage is not None: # 输入是文件，指定目标语言
        Log.debug("keyIndex = %s moduleIndex = %s languageIndex = %s"%(keyIndex,moduleIndex,tempLanguageIndex))
           # 获取 value 集合，并删除 title 项
        xmlValues = sheet.col_values(tempLanguageIndex)
        del xmlValues[0]
        
        XMLParse.update_xml_value(filePath, xmlKeys, xmlValues)
        return

    Log.debug("Not file")

    if dirPath is None: # 目录为空，返回
        Log.error("Error：输入不合法")
        return

    if not os.path.exists(dirPath):
        Log.error("Error：目标目录不存在")
        return
    
    for index, title in enumerate(fristRow):
        if index < fromIndex:
            continue
        languageIndex = index
        targetLanguage = title
        # print languageIndex
        # print title
        xmlValues = sheet.col_values(languageIndex)
        del xmlValues[0]
        # 文件路径（子目录） 比如; value-zh
        # ├── andorid
        # │   ├── values-zh
        # │   |	├── strings_device.xml
        # │   |	├── strings_me.xml
        # │   |	├── strings_moment.xml
        # │   ├── values-de
        # │   ├── values-ko
        sub_dir_path = covertTargetPath(dirPath, targetLanguage)
        if os.path.exists(sub_dir_path):
            XMLParse.update_mutixml_value(sub_dir_path, xmlKeys, xmlValues, xmlModules)


def main():
     options = addParser()
     xls2xml(options)
     Log.info("Done!")

# 读取 xls
main()