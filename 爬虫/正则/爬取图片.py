import requests
import re
import time
import os
from urllib import parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}

# 用request.get方法访问网址得到网页HTML内容
main_url = 'https://www.vmgirls.com/14931.html'
# main_url= 'https://www.vmgirls.com/12985.html'
response = requests.get(main_url, headers=headers)
# print(response.text)
# 网页内容以文本形式打印出来
html = response.text

# 为文件夹起名字用图片的名字命名
dir_name = re.findall('<h1 class="post-title h1">(.*?)</h1>', html)[-1]
print(dir_name)
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

# 获取图片地址
urls = re.findall('<a href="(.*?)" alt=".*?" title=".*?">', html)
# print(urls)

# 通过for循环来遍历筛选过的urls，然后分别下载保存
for url in urls:
    url = parse.urljoin('http://www.vmgirls.com/', url)
    file_name = url.split('/')[-1]
    response = requests.get(url, headers=headers)
    with open(dir_name + '/' + file_name, 'wb') as f:
        f.write(response.content)
