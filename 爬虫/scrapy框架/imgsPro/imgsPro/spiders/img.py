import scrapy
from imgsPro.items import ImgsproItem


class ImgSpider(scrapy.Spider):
    name = 'img'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://sc.chinaz.com/tupian/',
                  'https://sc.chinaz.com/tupian/fengjingtupian.html',
                  'https://sc.chinaz.com/tupian/huangsetupian.html']

    def parse(self, response):
        div_list = response.xpath('//div[@id="container"]/div')
        for div in div_list:
            # 注意：使用伪属性
            # //*[@id="container"]/div[1]/div/a/img/@src
            # 注意，本网站图片是懒加载，只有可视化区域内img的属性才是src，不在可视化范围内的是伪属性src2，
            # 只有浏览器鼠标滑动到可视范围内才会动态刷新属性为src，xpath要解析伪属性src2
            src = 'https:' + div.xpath('./div/a/img/@src2').extract_first()

            item = ImgsproItem()
            item['src'] = src

            yield item
