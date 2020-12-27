# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapystudyPipeline:
    fp = None

    # 重写父类打开文件的方法
    def open_spider(self, spider):
        self.fp = open('./段子.txt', 'w', encoding='utf-8')
        print('开始爬虫 ...')

    def close_spider(self, spider):
        print('爬虫结束！！！')
        self.fp.close()

    # 专门用来处理item类型对象
    # process_item方法接收爬虫文件提交过来的item对象,每收到一个item对象，就被调用一次
    def process_item(self, item, spider):
        # print(f'process_item {item}')
        author = item['author']
        content = item['content']
        self.fp.write(author + ':' + content + '\n')
        return item
