# Scrapy settings for jiazhang project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'jiazhang'

SPIDER_MODULES = ['jiazhang.spiders']
NEWSPIDER_MODULE = 'jiazhang.spiders'
ITEM_PIPELINES = [
    'jiazhang.pipelines.JiazhangPipeline',
]
#if os.path.exists('thisistest.path'):
MONGODB_URI = 'mongodb://jz100:Ckui87rJhCFDTZBH@115.28.39.237:10088/jz100'
#else:
    #MONGODB_URI = 'mongodb://192.168.123.101:27017'

MONGODB_DATABASE = "jiazhangdb"
MONGODB_COLLECTION = "jiazhangluntan"
MONGODB_UNIQUE_KEY = 'url'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jiazhang (+http://www.yourdomain.com)'
