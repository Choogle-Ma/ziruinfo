# -*- coding: utf-8 -*-
import scrapy, logging,  json
import time

hosturl = "https://weread.qq.com/"


class ZiroomSpider(scrapy.Spider):
    name = "ziroom"
    allowed_domains = ["ziroom.com"]

    def start_requests(self):
        url_root = "https://weread.qq.com/web/bookListInCategory/"
        requests = []

        for category in CATEGORY_COUNT:
            totalcount = CATEGORY_COUNT[category]
            page = 1000//20 + 1
            for i in range(1, page):
                maxindex = 20 * i
                url_t = url_root + str(category) + '?maxIndex=' + str(maxindex)
                request = scrapy.Request(url=url_t, callback=self.parse, meta={'category': category, 'index': maxindex})
                requests.append(request)

        return requests

    def parse(self, response):
        # logging.info(response.text)
        item = WereadItem()
        item['category'] = response.meta['category']
        item['index'] = response.meta['index']

        data = json.loads(response.text)
        item['books'] = data['books']
        item['synckey'] = data['synckey']
        item['hasMore'] = data['hasMore']
        item['totalCount'] = data['totalCount']

        yield item
