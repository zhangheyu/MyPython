import scrapy
from wangYiNews.items import WangyinewsItem
from selenium import webdriver


# scrapy crawl wangyi

class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    # allowed_domains = ['http://163.com']
    start_urls = ['https://news.163.com/']
    models_urls = []  # 存储五个板块对应详情页的url
    # 实例化一个浏览器对象， 用于中间件使用selenium获取异步返回的数据
    def __init__(self):
        self.bro = webdriver.Chrome(executable_path='E:\WORK\MyPython\爬虫\chromedriver.exe')

    def parse(self, response):
        # 解析五大板块对应详情页的url
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[1]/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        alist = [3, 4, 6, 7, 8]
        for index in alist:
            model_url = li_list[index].xpath('./a/@href').extract_first()
            self.models_urls.append(model_url)

        # 依次对每一个板块对应的页面进行请求
        for url in self.models_urls:  # 对每一个板块的url进行请求发送
            yield scrapy.Request(url, callback=self.parse_model)

    # 每一个板块对应的新闻标题相关的内容都是动态加载
    def parse_model(self, response):  # 解析每一个板块页面中对应新闻的标题和新闻详情页的url
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            new_detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
            # new_detail_url = str(new_detail_url)
            print(f'new_url:{new_detail_url}')
            # 详情页url有可能为空，extract_first会返回None，导致运行报错
            if new_detail_url is not None:

                item = WangyinewsItem()
                item['title'] = title

                # 对新闻详情页的url发起请求
                yield scrapy.Request(url=new_detail_url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):  # 解析新闻内容
        content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
        content = ''.join(content)
        item = response.meta['item']
        item['content'] = content

        yield item

    def closed(self, spider):
        self.bro.quit()
