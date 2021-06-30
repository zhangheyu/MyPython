import re


input_psd = input("请输入字符串:")
test_str = re.search(r"[^a-zA-Z_\-\d\.]", input_psd)
if test_str is None:
    print("没有没有真没有特殊字符")
else:
    print("只允许录入英文字母、数字、_、-、.")
