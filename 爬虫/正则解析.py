import requests
import json
import re
import os
import time
from fake_useragent import UserAgent

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}

# ua = UserAgent()
# headers = {"User-Agent": ua.random}


def get_image_urls(page_url):
    page_data = requests.get(url=page_url, headers=headers)
    # print(page_data.text)
    # with open('page.html', 'w', encoding='utf-8') as fd:
    #     fd.write(page_data.text)
    image_urls = re.findall('<img src="(.*?)" />', page_data.text)
    # print(image_urls)
    return image_urls


def download_image(dir_name, image_url):
    print(image_url)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    for url in image_url:
        # url ='https://85cjg.com/upload/image/20200807/1596815568448096.jpg'
        url = 'https://85cjg.com' + url
        file_name = url.split('/')[-1]
        try:
            resp = requests.get(url=url, headers=headers)
        except:
            continue

        if not os.path.exists(dir_name + '/' + file_name):
            with open(dir_name + '/' + file_name, 'wb') as fd:
                # # content:返回的二进制数据， text:返回的字符串数据， json：返回的json格式才可用
                fd.write(resp.content)
                print(f'download {file_name} done')
        else:
            print(f'{file_name}已经存在')
        time.sleep(0.5)

if __name__ == '__main__':

    zbj_url = 'https://85cjg.com/index/imgs/id/2294.html'
    aj_url = 'https://85cjg.com/index/imgs/id/2293.html'
    cwy_url = 'https://85cjg.com/index/imgs/id/2291.html'
    菊川みつ葉 = 'https://85cjg.com/index/imgs/id/2225.html'
    # print('获取zbz图片url')
    # image_urls = get_image_urls(zbj_url)
    # print('下载zbz图片')
    # download_image('zbj', image_urls)
    # print('下载zbz图片完成')

    # print('获取aj图片url')
    # image_urls = get_image_urls(aj_url)
    # print('下载aj图片')
    # download_image('aj', image_urls)
    # print('下载aj图片完成')

    # print('获取cwy图片url')
    # image_urls = get_image_urls(cwy_url)
    # print('下载cwy_url图片')
    # download_image('cwy', image_urls)
    # print('下载cwy图片完成')

    # print('获取菊川みつ葉图片url')
    # image_urls = get_image_urls(菊川みつ葉)
    # print('下载菊川みつ葉图片')
    # download_image('菊川みつ葉', image_urls)
    # print('下载菊川みつ葉图片完成')
