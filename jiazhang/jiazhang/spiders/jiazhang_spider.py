from scrapy.spider import Spider
import re
import time
from datetime import datetime
from scrapy.selector import Selector
from scrapy.http import Request
from jiazhang.items import JiazhangItem


class JiazhangSpider(Spider):
    name = "jiazhang"
    start_urls = [
        'http://www.jz100.com/forum-4-1.html',
    ]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        """
        sel = Selector(response)
        sites = sel.xpath('//form/table//tbody[contains(@id, "normalthread")]//th[@class="new"]')
        items = []

        for site in sites:
            item = {}
            name =  site.xpath('a/text()').extract()[0]
            url = site.xpath('a/@href').extract()[0]
            print name, url
            yield Request(url, callback=self.parse_detail)
            items.append(item)

    def parse_detail(self, response):
        result = JiazhangItem()
        sel = Selector(response)
        url = response.url
        result.setdefault('url', url)
        title = sel.xpath('//span[@id="thread_subject"]/text()').extract()[0]
        result.setdefault('title', title)
        result.setdefault('data', [])
        sites1 = sel.xpath('//td[contains(@id, "postmessage")]')
        sites2 = sel.xpath('//div[contains(@id, "favatar")]//div[@class="authi"]')
        sites3 = sel.xpath('//em[contains(@id, "authorposton")]')
        for site1, site2, site3 in zip(sites1, sites2, sites3):
            data = site1.xpath('descendant-or-self::*/text()').extract()
            string = ' '.join(data)
            name =  site2.xpath('a/text()').extract()[0]
            #url = item['url'] = site.xpath('a/@href').extract()[0]
            createtime = site3.xpath('text()').extract()[0]
            strtime = re.compile('(\d{4}-\d*-\d* \d*:\d*)').findall(createtime)[0]
            createtime = time.mktime(datetime.strptime(strtime, '%Y-%m-%d %M:%S').timetuple())

            result['data'].append({'name':name, 'createtime':createtime, 'string':string})
            break
        return result
