# -*- coding: utf-8 -*-
import scrapy, logging, json
from ziru.items import CommunityInfoItem, CommunityItem


class ZiroomSpider(scrapy.Spider):
    name = "community"
    allowed_domains = ["ziroom.com"]

    def start_requests(self):
        url_sample = "http://www.ziroom.com/xiaoqu/1111027375969.html"
        url_root = "http://www.ziroom.com/xiaoqu/"
        requests = []

        with open(r'/home/mahj/PycharmProjects/ziruinfo/ziru/files/community.json', 'r') as f:
            data = json.load(f)

        communities = {}
        for i in data:
            if i['data'] != []:
                for community in i['data']:
                    communities[community['code']] = community['name']

        for c in communities:
            url_t = url_root + c + ".html"

            request = scrapy.Request(url=url_t, callback=self.parse,
                                     meta={'community_id': c, 'community_name': communities[c]})

            requests.append(request)

        return requests

    def parse(self, response):
        # logging.info(response.text)
        item = CommunityInfoItem()
        item['id'] = response.meta['community_id']
        item['name'] = response.meta['community_name']
        # data = response.xpath("//div[@class='Z_look']/div/div/div/div[@class='item']/p").extract()

        data = response.xpath("//div[@class='Z_look']/div/div[@class='item']/p/text()").extract()
        for i in data:
            # logging.info("Test")
            # logging.info(i.strip())
            info = i.strip()
            if '建筑年代' in info:
                item['build_time'] = info.split('：')[1]
            elif '建筑类型' in info:
                item['build_type'] = info.split('：')[1]
            elif '建筑面积' in info:
                item['build_area'] = info.split('：')[1]
            elif '绿化率' in info:
                item['landscaping'] = info.split('：')[1]
            elif '容积率' in info:
                item['FAR'] = info.split('：')[1]
            elif '小区是否有噪音（毗邻车站机场）' in info:
                item['is_noise'] = info.split('：')[1]
            elif '车位配比' in info:
                item['park_v'] = info.split('：')[1]
            elif '停车费(月)' in info:
                item['park_month'] = info.split('：')[1]
            elif '停车费(年)' in info:
                item['park_year'] = info.split('：')[1]
            elif '车位是否出租' in info:
                item['is_rent'] = info.split('：')[1]
            elif '小区充电桩' in info:
                item['has_power'] = info.split('：')[1]

        # logging.info(response.body)

        yield item
