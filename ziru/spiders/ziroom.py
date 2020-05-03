# -*- coding: utf-8 -*-
import scrapy, logging, json
from ziru.items import ZiruItem, CommunityItem

hosturl = "https://weread.qq.com/"


class ZiroomSpider(scrapy.Spider):
    name = "ziroom"
    allowed_domains = ["ziroom.com"]

    def start_requests(self):
        url_sample = "http://www.ziroom.com/map/room/count?min_lng=116.206912&max_lng=116.216398&min_lat=39.947775&max_lat=39.949351&clng=116.211655&clat=39.948563&zoom=18"
        url_root = "http://www.ziroom.com/map/room/count?"
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

        lng_t = (lng_west + lng_east)/2
        # lng_t = lng_west
        zoom = 18

        while lng_t < lng_east:
            lng_t_min = lng_t
            lng_t_max = lng_t + delta_lng
            clng_t = (lng_t_min + lng_t_max) / 2

            lat_t = (lat_south + lat_north)/2
            # lat_t = lat_south
            while lat_t < lat_north:
                lat_t_min = lat_t
                lat_t_max = lat_t + delta_lat
                clat_t = (lat_t_max + lat_t_min) / 2

                url_t = url_root + "min_lng=%f&max_lng=%f&min_lat=%f&max_lat=%f&clng=%f&clat=%f&zoom=%d" % \
                        (lng_t_min, lng_t_max, lat_t_min, lat_t_max, clng_t, clat_t, zoom)

                request = scrapy.Request(url=url_t, callback=self.parse)
                requests.append(request)

                lat_t = lat_t_max

            lng_t = lng_t_max

        return requests

    def parse(self, response):
        # logging.info(response.text)
        item = ZiruItem()

        data = json.loads(response.text)
        item['return_code'] = data['code']
        item['message'] = data['message']
        item['data'] = data['data']

        yield item
