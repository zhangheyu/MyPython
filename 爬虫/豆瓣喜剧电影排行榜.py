import requests
import json
url = 'https://movie.douban.com/j/chart/top_list'
param = {
    'type': '24',
    'interval_id': '100:90',
    'action': '',
    'start': 1,
    'limit:': 50
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}
response = requests.get(url=url, params=param, headers=headers)
# print(response.json())
list_data = response.json()
fd = open('豆瓣喜剧电影排行前50.json', 'w', encoding='utf-8')
json.dump(list_data, fp=fd, ensure_ascii=False)
fd.close()

print('over')
