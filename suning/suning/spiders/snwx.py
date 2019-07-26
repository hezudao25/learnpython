# -*- coding: utf-8 -*-
import scrapy
import copy

class SnwxSpider(scrapy.Spider):
    name = 'snwx'
    allowed_domains = ['suning.com']
    start_urls = ['https://list.suning.com/0-502319-0.html?safp=d488778a.46602.crumbs.3#search-path']

    def parse(self, response):
        dd_list = response.xpath("//div[@id='search-path']/dl/dd/a")
        for dd in dd_list:
            items = {}
            items["s_title"] = dd.xpath("./@title").extract_first()
            items["s_href"] = dd.xpath("./@href").extract_first()
            items["s_href"] = "https:" + items["s_href"]

            if items["s_href"] is not None:
                yield scrapy.Request(items["s_href"], callback=self.parse_content_list, meta={'item': copy.deepcopy(items)})

    def parse_content_list(self, response):
        items = response.meta["item"]
        div_list = response.xpath("//div[@id='product-list']/ul/li/div/div")
        for div in div_list:
            items["book-title"] = div.xpath(".//div[@class='title-selling-point']/a/@title").extract_first()
            items["book-img"] = div.xpath(".//div[@class='res-img']/div/a/img/@src").extract_first()
            items["book-author"] = div.xpath(".//em[@class='book-author']/text()").extract_first()
            items["book-press"] = div.xpath(".//em[@class='book-press']/text()").extract_first()
            items["book-time"] = div.xpath(".//em[@class='book-time']/text()").extract_first()
            items["book-price"] = div.xpath("./div/div/span[@class='def-price']/descendant::text()").extract()
            items["book-href"] = div.xpath(".//div[@class='title-selling-point']/a/@href").extract_first()
            items["book-href"] = "https:" + items["book-href"]

            yield items

