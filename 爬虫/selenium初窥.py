from time import sleep
from selenium import webdriver
from lxml import etree

# http://scxk.nmpa.gov.cn:81/xk/  食品药监总局网址

if __name__ == '__main__':
    # 实例化一个浏览器对象（传入浏览器的驱动）
    bro = webdriver.Chrome(executable_path="./chromedriver.exe")
    # 让浏览器发起一个指定url的请求
    bro.get('http://scxk.nmpa.gov.cn:81/xk/')
    # page_source获取浏览器当前页面的源码数据
    page_text = bro.page_source
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//ul[@id="gzlist"]')[0]
    for li in li_list:
        name = li.xpath('./dl/@title')[0]
        print(name)
    sleep(5)
    bro.quit()
