import scrapy
from imageSpider.items import ImagespiderItem

class ScrapyimagedownloadSpider(scrapy.Spider):
    name = 'scrapyImageDownload'
    # allowed_domains = ['https://sc.chinaz.com/tupian/']
    start_urls = ['https://sc.chinaz.com/tupian/']

    def parse(self, response):
        div_list = response.xpath('//div[@id="container"]/div')
        for div in div_list:
            # //*[@id="container"]/div[1]/div/a/img/@src
            # 注意，本网站图片是懒加载，只有可视化区域内img的属性才是src，不在可视化范围内的是伪属性src2，
            # 只有浏览器鼠标滑动到可视范围内才会动态刷新属性为src，xpath要解析伪属性src2
            src = 'https:' + div.xpath('./div/a/img/@src2').extract_first()
            print(src)

            item = ImagespiderItem()
            item['src'] = src

            yield item
