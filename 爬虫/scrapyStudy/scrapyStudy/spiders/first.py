import scrapy


class FirstSpider(scrapy.Spider):
    # 爬虫文件的名称，就是爬虫源文件的唯一标识符
    name = 'first'
    # 允许的域名，用来限定start_urls列表中哪些url可以进行请求发送，一般不使用
    # allowed_domains = ['study.com']
    # 起始的url列表，该列表中的url会被scrapy自动进行请求的发送
    start_urls = ['https://www.baidu.com', 'https://www.sogou.com/']

    # 用于数据解析，response返回请求成功后对应的数据
    def parse(self, response):
        # pass
        print(response)
