import requests

post_url = 'https://fanyi.baidu.com/sug'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}

while True:
    world = input('请输入要翻译的单词:')
    data = {
        'kw': world
    }
    if len(world) == 0:
        continue

    response = requests.post(url=post_url, data=data, headers=headers)
    # print(response.text)
    # print(response.headers['Content-Type'])
    resp_content_type = response.headers['Content-Type']

    if resp_content_type.find('json'):
        dict_obj = response.json()
        trans = dict_obj['data']
    else:
        trans = response.text()

    print(f'单词 {world} 翻译后的内容是:\n {trans}')
