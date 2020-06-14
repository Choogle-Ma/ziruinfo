# -*- coding: utf-8 -*-
import scrapy, logging, json
from ziru.items import ZiruItem, CommunityItem, RentItem


class ZiroomSpider(scrapy.Spider):
    name = "getrent"
    allowed_domains = ["ziroom.com"]

    def start_requests(self):
        url_sample = "http://www.ziroom.com/map/room/list?min_lng=116.206912&max_lng=116.216398&min_lat=39.947775&max_lat=39.949351&clng=116.211655&clat=39.948563&zoom=18"
        url_root = "http://www.ziroom.com/map/room/list?"
        requests = []

        """
        经线
        西：116.097839
        东：116.718748
        南：39.716082
        北：40.180713
        
        东西跨度：0.620909，70
        南北跨度：0.464631，142
        """

        lat_north = 40.180713
        lat_south = 39.716082
        lng_west = 116.097839
        lng_east = 116.718748

        delta_lng = 0.008961
        delta_lat = 0.003293

        # lng_t = (lng_west + lng_east)/2
        lng_t = lng_west
        zoom = 18

        while lng_t < lng_east:
            lng_t_min = lng_t
            lng_t_max = lng_t + delta_lng
            clng_t = (lng_t_min + lng_t_max) / 2

            # lat_t = (lat_south + lat_north)/2
            lat_t = lat_south
            while lat_t < lat_north:
                lat_t_min = lat_t
                lat_t_max = lat_t + delta_lat
                clat_t = (lat_t_max + lat_t_min) / 2

                url_t = url_root + "min_lng=%f&max_lng=%f&min_lat=%f&max_lat=%f&clng=%f&clat=%f&zoom=%d&p=1&area=40,100&type=11" % \
                        (lng_t_min, lng_t_max, lat_t_min, lat_t_max, clng_t, clat_t, zoom)

                request = scrapy.Request(url=url_t, callback=self.parse,
                                         meta={'url_root': url_root, 'lng_t_min': lng_t_min, 'lng_t_max': lng_t_max,
                                               'lat_t_min': lat_t_min, 'lat_t_max': lat_t_max, 'clng_t': clng_t,
                                               'clat_t': clat_t, 'zoom': zoom})
                yield request
                # requests.append(request)

                lat_t = lat_t_max

            lng_t = lng_t_max

        # return requests

    def parse(self, response):
        # logging.info(response.text)
        item = RentItem()

        data = json.loads(response.text)
        item['return_code'] = data['code']
        item['message'] = data['message']
        item['rooms'] = data['data']['rooms']
        item['total'] = data['data']['total']
        item['pages'] = data['data']['pages']

        url_root = response.meta['url_root']
        lng_t_min = response.meta['lng_t_min']
        lng_t_max = response.meta['lng_t_max']
        lat_t_min = response.meta['lat_t_min']
        lat_t_max = response.meta['lat_t_max']
        clng_t = response.meta['clng_t']
        clat_t = response.meta['clat_t']
        zoom = response.meta['zoom']

        if item['pages'] > 1:
            for i in range(2, item['pages']+1):
                url_t = url_root + "min_lng=%f&max_lng=%f&min_lat=%f&max_lat=%f&clng=%f&clat=%f&zoom=%d&p=%d&area=40,100&type=11" % \
                        (lng_t_min, lng_t_max, lat_t_min, lat_t_max, clng_t, clat_t, zoom, i)

                request = scrapy.Request(url=url_t, callback=self.parse_more)
                yield request
        else:

            yield item

    def parse_more(self, response):

        item = RentItem()

        data = json.loads(response.text)
        item['return_code'] = data['code']
        item['message'] = data['message']
        item['rooms'] = data['data']['rooms']
        item['total'] = data['data']['total']
        item['pages'] = data['data']['pages']

        yield item
