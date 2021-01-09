import scrapy
from scrapyStudy.items import ScrapystudyItem


class FirstSpider(scrapy.Spider):
    # 爬虫文件的名称，就是爬虫源文件的唯一标识符
    name = 'first'
    # 允许的域名，用来限定start_urls列表中哪些url可以进行请求发送，一般不使用
    # allowed_domains = ['study.com']
    # 起始的url列表，该列表中的url会被scrapy自动进行请求的发送
    start_urls = ['https://www.qiushibaike.com/text/']

    # 用于数据解析，response返回请求成功后对应的数据
    # 基于管道存储爬取到的数据
    def parse(self, response):
        # 解析作者的名字+段子内容
        div_list = response.xpath('//*[@id="content"]/div/div[2]/div')
        for div in div_list:
            # xpath返回的是列表，但列表类型一定是Selector类型的对象
            # [<Selector xpath='./div[1]/a[2]/h2/text()' data='\n无书斋主\n'>]
            # extract()可以将Selector对象的data存储的字符串提取出来
            author = div.xpath('./div[1]/a[2]/h2/text() | ./div[1]/span/h2/text()')[0].extract()
            # 列表调用了extract()后，则表示将列表中每一个selector对象中data对应的字符串提取出来
            content = div.xpath('./a[1]/div/span/text()').extract()
            content = ''.join(content)
            # print(f'作者：{author.strip()}\t段子：{content.strip()}')
            item = ScrapystudyItem()
            item['author'] = author.strip()
            item['content'] = content.strip()
            yield item  # 将item提交给管道

    # 基于终端指令持久化存储
    def parse_cmd(self, response):
        # 解析作者的名字+段子内容
        div_list = response.xpath('//*[@id="content"]/div/div[2]/div')
        # print(len(div_list))
        all_data = []  # 用于终端指令持久化存储parse返回的内容
        for div in div_list:
            # print(div)
            # xpath返回的是列表，但列表类型一定是Selector类型的对象
            # [<Selector xpath='./div[1]/a[2]/h2/text()' data='\n无书斋主\n'>]
            # extract()可以将Selector对象的data存储的字符串提取出来
            author = div.xpath('./div[1]/a[2]/h2/text()')[0].extract()
            # 列表调用了extract()后，则表示将列表中每一个selector对象中data对应的字符串提取出来
            content = div.xpath('./a[1]/div/span/text()').extract()
            content = ''.join(content)
            # print(f'作者：{author.strip()}\t段子：{content.strip()}')
            data = {
                '作者': author.strip(),
                '段子': content.strip()
            }
            all_data.append(data)
            print(data)
        return all_data
        # scrapy crawl first -o 段子.csv/json/xml/pickle/jl 存储parse返回的数据
