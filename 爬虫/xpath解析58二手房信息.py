import requests
from fake_useragent import UserAgent
from lxml import etree

ua = UserAgent()

if __name__ == '__main__':
    headers = {"User-Agent": ua.random}
    page_url = 'https://cd.58.com/ershoufang/'
    page_text = requests.get(url=page_url, headers=headers).text
    # 数据解析
    tree = etree.HTML(page_text)
    # 解析页面的li标签存储到列表
    li_list = tree.xpath('//div/ul[@class="house-list-wrap"]/li')
    fp = open("58二手房信息.txt", 'w', encoding='utf-8')
    for li in li_list:
        # 局部标签解析
        title = li.xpath('./div[2]/h2/a/text()')[0]
        area = li.xpath('./div[2]/p/span[2]/text()')[0]
        price = li.xpath('./div[3]/p/b/text()')[0]
        print(f'{title} 面积 {area} 价格 {price}万')
        fp.write(title + '面积' + area + ' 价格' + price + '万' + '\n')
    fp.close()
