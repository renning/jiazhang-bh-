# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import tornado.escape
from pymongo import errors
from scrapy_mongodb import MongoDBPipeline


#from scrapy.exception import DropItem
from scrapy.conf import settings
from scrapy import log

class JiazhangPipeline(MongoDBPipeline):
    def insert_item(self, item, spider):
        """ Process the item and add it to MongoDB

        :type item: (Item object) or [(Item object)]
        :param item: The item(s) to put into MongoDB
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: Item object
        """
        if not isinstance(item, list):
            item = dict(item)

            if self.config['append_timestamp']:
                item['scrapy-mongodb'] = {'ts': datetime.datetime.utcnow()}

        if self.config['unique_key'] is None:
            try:
                self.collection.insert(item, continue_on_error=True)
                log.msg(
                    'Stored item(s) in MongoDB {0}/{1}'.format(
                        self.config['database'], self.config['collection']),
                    level=log.DEBUG,
                    spider=spider)
            except errors.DuplicateKeyError:
                log.msg('Duplicate key found', level=log.DEBUG)
                if (self.stop_on_duplicate > 0):
                    self.duplicate_key_count += 1
                    if (self.duplicate_key_count >= self.stop_on_duplicate):
                        self.crawler.engine.close_spider(
                            spider,
                            'Number of duplicate key insertion exceeded'
                        )
                pass

        else:
            self.collection.update(
                {
                    self.config['unique_key']: item[self.config['unique_key']]
                },
                item,
                upsert=True)
            log.msg(
                'Stored item(s) in MongoDB {0}/{1}'.format(
                    self.config['database'], self.config['collection']),
                level=log.DEBUG,
                spider=spider)

