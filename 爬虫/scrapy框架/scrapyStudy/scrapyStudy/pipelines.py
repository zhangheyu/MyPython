# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


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
        return item  # 会传递给下一个即将执行的管道类


# 管道文件中一个管道类代表将数据存储到一个平台或载体中
class mysqlPipeline:
    conn = None
    cursor = None

    def open_spider(self, spider):
        print('创建数据库 ...')
        try:
            self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='password', db='Dubai',
                                        charset='utf8')  #建立数据库连接
        except Exception as e:
            print(f'连接数据库失败{e}')

    def close_spider(self, spider):
        print('关闭数据库！！！')
        self.conn.close()
        self.cursor.close()

    def process_item(self, item, spider):
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute('insert into Dubai values("%s","%s")' % (item["author"], item["content"]))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item  # 会传递给下一个即将执行的管道类
