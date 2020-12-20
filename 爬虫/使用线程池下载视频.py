import re
import requests
from lxml import etree
from multiprocessing.dummy import Pool

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}
urls = []


def get_video_urls(url):
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//*[@id="categoryList"]/li')
    for li in li_list:
        detail_url = 'https://www.pearvideo.com/' + li.xpath('./div/a/@href')[0]
        name = li.xpath('./div/a/div[2]/text()')[0] + '.mp4'
        # print(detail_url, name)
        # detail_text = requests.get(url=detail_url, headers=headers).text
        # ex = 'srUrl="(.*?)",vdoUrl'
        # v = re.findall(ex, detail_text)
        # print(v)
        # 视频详细链接是通过ajax异步返回的，直接对详情链接请求拿不到
        # https://www.pearvideo.com/videoStatus.jsp?contId = 1712055 & mrd = 0.9553228586655185
        session = requests.Session()
        response = session.get(detail_url, headers=headers)
        cookie = response.cookies
        # print(cookie)
        ajax_url = 'https://www.pearvideo.com/videoStatus.jsp'
        contId = detail_url.split('_')[-1]
        # print(contId)
        # headers中加入Referer至关重要，这是最重要的反反爬的一步
        headers['Referer'] = 'https://www.pearvideo.com/video_' + contId
        param = {
            'contId': contId,
            'mrd': ''
        }
        # cookies也可以不加
        video_json = requests.get(url=ajax_url, params=param, headers=headers, cookies=cookie).json()
        # print(video_detail_json)
        # srcUrl = video_detail_json['videoInfo']['videos']['srcUrl']

        #  由于反爬机制，要对拿到的视频url做处理
        mp4_js = video_json['videoInfo']['videos']['srcUrl']  # 获取srcUrl地址
        img_js = video_json['videoInfo']['video_image']  # 获取video_image地址
        img_msg = img_js.split('/')[-1]
        # 获取img_js的一部分cont-1703049
        cont = re.findall('(.*?-.*?)-.*?', img_msg)[0]
        mp4_list = re.split('//|/', mp4_js)
        # 将后面的地址修改
        mp4_list[-1] = re.sub('\d+', cont, mp4_list[-1], count=1)  # 替换第一组的数字
        # 拼接成真实地址
        new_video = mp4_list[0] + '//' + '/'.join(mp4_list[1:])

        dic = {
            'name': name,
            'url': new_video
        }
        urls.append(dic)


def download_video(dic):
    url = dic['url']
    video_data = requests.get(url=url, headers=headers).content
    path = '梨视频/' + dic['name']
    with open(path, 'wb') as fd:
        fd.write(video_data)
        print(f"{dic['name']} 下载完成！！！")


if __name__ == '__main__':
    url = 'https://www.pearvideo.com/category_5'
    get_video_urls(url)
    print(urls)
    # 使用线程池下载视频（较为耗时的操作）
    pool = Pool(4)
    pool.map(download_video, urls)
    pool.close()
    pool.join()
