import requests

url = 'https://www.baidu.com/s'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}
kw = input('请输入要搜索的内容：')
param = {
    'wd': kw
}

response = requests.get(url=url, params=param, headers=headers)
# print(response.text)

with open(kw + '.html', 'w', encoding='utf-8') as fd:
    fd.write(response.text)

fd.close()
