import os
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}
if __name__ == '__main__':
    url = 'http://pic.netbian.com/4kmeinv/'
    # 可以手动设定响应数据的编码格式，解决中文乱码
    response = requests.get(url=url, headers=headers)
    # response.encoding = 'utf-8'
    page_text = response.text

    tree = etree.HTML(page_text)
    li_list = tree.xpath('//div[@class="slist"]/ul/li')
    # 解析img标签的src属性用于下载图片，alt属性作为图片名字
    if not os.path.exists('彼岸图网'):
        os.mkdir('彼岸图网')

    for li in li_list:
        image_src = 'http://pic.netbian.com' + li.xpath('./a/img/@src')[0]
        # 通用解决中文乱码的解决方案
        image_name = li.xpath('./a/img/@alt')[0]
        image_name = image_name.encode('iso-8859-1').decode('gbk')
        # print(image_name, image_src)
        image_data = requests.get(url=image_src, headers=headers).content
        file_path = '彼岸图网/' + image_name + '.jpg'
        with open(file_path, 'wb') as fd:
            fd.write(image_data)
            print(f'下载{image_name}成功！！！')
            fd.close()
