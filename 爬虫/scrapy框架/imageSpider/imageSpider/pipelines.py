# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline

# class ImagespiderPipeline:
#     def process_item(self, item, spider):
#         return item

# 使用scrapy定义的ImagesPipeline类下载图片
class imgsPileLine(ImagesPipeline):
    # 根据图片地址进行图片数据的请求
    def get_media_requests(self, item, info):
        print(f"url:{item['src']}")
        yield scrapy.Request(item['src'])

    # 指定图片存储的路径
    def file_path(self, request, response=None, info=None):
        print(f'name:{imgName}')
        imgName = request.url.split('/')[-1]
        return imgName

    def item_completed(self, results, item, info):
        return item  # 返回给下一个即将被执行的管道类
