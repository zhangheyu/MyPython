import requests
from bs4 import BeautifulSoup
import time
import json
import os

if __name__ == '__main__':
    # 1、本地html文件初始化,soup常用操作
    print('bs4解析本地html文件')
    fd = open('test_bs4.html', 'r', encoding='utf-8')
    soup = BeautifulSoup(fd, 'lxml')
    # print(soup)
    # soup.TagName返回的是文档中第一次出现的TagName对应的标签
    # print(soup.p)  # 打印的是html中p标签第一出现的内容
    # soup.find():等同于soup.TagName
    # print(soup.find('p'))   # 打印的是html中p标签第一出现的内容
    # print(soup.find('p', class_="second"))  #属性定位，返回class="second"对应的标签
    # soup.findall('TagName'), 查找所有的TagName对应的标签
    # print(soup.find_all('p'))  #以列表的形式返回所有的p标签
    # select('某种选择器(id/class/标签)')，以列表形式返回
    # print(soup.select('#music'))  # 返回id="music"的标签
    # print(soup.select('.text'))  # 返回class="text"的标签内容
    # select层级选择器,一个>表示一个层级, 空格表示多个层级
    # print(soup.select('.text > p')[1])  # 返回属性class="text"的标签下的第二个p标签对于的内容
    # 获取标签之间的文本数据soup.TagNmae.text/string/get_text()
    # text/get_text()获取某个标签中所有的文本内容(每一层),string只可获取此标签下面的直系文本内容
    # print(soup.div.text)
    # print(soup.p.string)
    # print(soup.p.get_text())
    # 获取标签中属性值
    # print(soup.select('#music')[0]['src'])
