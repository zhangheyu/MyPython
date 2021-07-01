# -*encoding:utf-8*-
import re

input_psd = input("请输入字符串:")
test_str = re.search(r"[^a-zA-Z_\-\d\.]", input_psd)  # re.search 扫描整个字符串并返回第一个成功的匹配

if test_str is None:
    print("没有没有真没有特殊字符")
else:
    print("只允许录入英文字母、数字、_、-、.")
    print("search到非法字符:{}".format(test_str[0]))

match_str = re.match(r"[^a-zA-Z_\-\d\.]", input_psd)  # re.match 尝试从字符串的起始位置匹配一个模式，如果不是起始位置匹配成功的话，match()就返回none
if match_str is None:
    print("match failed")
else:
    print("只允许录入英文字母、数字、_、-、.")
    print("match到非法字符:{}".format(test_str[0]))
