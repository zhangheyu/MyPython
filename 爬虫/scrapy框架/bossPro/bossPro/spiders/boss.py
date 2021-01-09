import scrapy
from bossPro.items import BossproItem
from urllib.parse import urlencode


class BossSpider(scrapy.Spider):
    name = 'boss'

    # allowed_domains = ['boss.com']
    # https://www.zhipin.com/c101270100-p100105/   boss
    # start_urls = ['https://www.lagou.com/zhaopin/qianrushi/']

    def start_requests(self):
        for page in range(1, 4):
            base_url = 'https://www.lagou.com/zhaopin/qianrushi/'
            params = {
                'filterOption': page,
                'sid': '5558b180170b42d5a088c051373311ed'
            }
            url = base_url + str(page) + '/' + urlencode(params)
            print(f'url={url}')
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        print('pass enter')
        # print(f'response:{response.text}')
        # boss 现在是xhr异步返回的，拿不到职位列表，爬取拉钩的数据
        li_list = response.xpath('//*[@id="s_position_list"]/ul/li')
        print(f'li_list:{len(li_list)}')
        for li in li_list:
            item = BossproItem()
            # //*[@id="main"]/div/div[3]/ul/li[3]/div/div[1]/div[1]/div/div[1]/span[1]/a    boss
            # //*[@id="s_position_list"]/ul/li[2]/div[1]/div[1]/div[1]/a/h3          拉钩
            # //*[@id="s_position_list"]/ul/li[8]/div[1]/div[1]/div[1]/a   拉钩
            job_name = li.xpath('./div[1]/div[1]/div[1]/a/h3/text()').extract_first()
            detail_url = li.xpath('./div[1]/div[1]/div[1]/a/@href').extract_first()
            item['job_name'] = job_name.strip()
            print(f'job_name:{job_name}')
            # 对详情页发请求获取职位详细描述
            # 手动发请求
            # 请求传参 meta={}可以将meta字典传给请求回调函数
            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item']
        # //*[@id="job_detail"]/dd[2]/div
        # //*[@id="job_detail"]/dd[2]/div
        # //*[@id="job_detail"]/dd[2]/div/br[7]
        # 异步响应，拿不到
        job_desc = response.xpath('//*[@id="job_detail"]/dd[2]/div//text()')
        # print(f'job_desc:{response.text}')
        # job_desc = ''.join(job_desc)
        item['job_desc'] = job_desc
        yield item
