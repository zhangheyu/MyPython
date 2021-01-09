import os
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}

if __name__ == '__main__':
    url = 'https://www.aqistudy.cn/historydata'
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    all_city_name = []
    # 热门城市li标签层级：'//div[@class="bottom"]/ul/li'
    # 全部城市li标签层级： '//div[@class="bottom"]/ul/div[2]/li'
    a_list = tree.xpath('//div[@class="bottom"]/ul/li/a | //div[@class="bottom"]/ul/div[2]/li/a')
    for a in a_list:
        city_name = a.xpath('./text()')[0]
        all_city_name.append(city_name)
    print(all_city_name)