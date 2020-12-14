import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

ua = UserAgent()

if __name__ == '__main__':
    print('使用bs4抓取三国演义所有的章节内容')
    url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
    headers = {"User-Agent": ua.random}
    page_text = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(page_text, 'lxml')
    # 解析章节标题和详情页url
    li_list = soup.select('.book-mulu > ul > li')
    fp = open('三国演义.txt', 'w', encoding='utf-8')
    print('解析章节标题和详情页url')
    for li in li_list:
        headers = {"User-Agent": ua.random}
        title = li.a.string
        detail_url = 'https://www.shicimingju.com' + li.a['href']
        # 对详情页发起请求,获取章节内容
        detail_page_text = requests.get(url=detail_url, headers=headers).text
        print('获取详情成功!')
        soup_detail = BeautifulSoup(detail_page_text, 'lxml')
        div_tag = soup_detail.find('div', class_='chapter_content')
        content = div_tag.text  # text返回所有的div标签的下层标签对应的文本
        # print(content)
        fp.write('\t\t\t\t\t' + title + content + '\n')
        print(f'爬取{title} 完成')
        time.sleep(0.5)
    fp.close()

