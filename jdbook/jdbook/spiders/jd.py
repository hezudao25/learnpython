# -*- coding: utf-8 -*-
import scrapy
import urllib
from copy import deepcopy
import json

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        big_list = response.xpath("//div[@class='mc']/dl/dt")
        for big in big_list:
            items = {}
            items["b_cate"] = big.xpath("./a/text()").extract_first()
            small_list = big.xpath("./following-sibling::dd[1]/em")
            for small in small_list:
                items["s_cate"] = small.xpath("./a/text()").extract_first()
                items["s_url"] = small.xpath("./a/@href").extract_first()
                items["s_url"] = urllib.parse.urljoin(response.url, items["s_url"])

                yield scrapy.Request(
                    items["s_url"],
                    callback=self.parse_content_list,
                    meta={"item": deepcopy(items)}
                                     )

    def parse_content_list(self, response):
        items = response.meta["item"]
        content_list = response.xpath("//ul[@class='gl-warp clearfix']/li")
        for content in content_list:
            items["book_pic"] = content.xpath(".//div[@class='p-img']//img/@src").extract_first()
            if items["book_pic"] is None:
                items["book_pic"] = content.xpath(".//div[@class='p-img']//img/@data-lazy-img").extract_first()
            items["book_pic"] = items["book_pic"] if items["book_pic"] is not None else None
            items["book_title"] = content.xpath(".//div[@class='p-name']//em/text()").extract_first()
            items["book_title"] = items["book_title"].strip()
            items["book_author"] = content.xpath(".//span[@class='p-bi-name']//a/text()").extract_first()
            items["book_store"] = content.xpath(".//span[@class='p-bi-store']//a/text()").extract_first()
            items["book_date"] = content.xpath(".//span[@class='p-bi-date']/text()").extract_first()
            items['book_sku'] = content.xpath("./div/@data-sku").extract_first()

            yield scrapy.Request(
                "https://p.3.cn/prices/mgets?skuIds=J_{}".format(items["book_sku"]),
                callback=self.parse_price,
                meta={"item": deepcopy(items)}
            )

            # 下一页
            next_url = response.xpath("//a[@class='pn-next']/@href").extract_first()
            if next_url is not None:
                next_url = urllib.parse.urljoin(response.url, next_url)
                yield scrapy.Request(next_url, callback=self.parse_content_list, meta={"item": deepcopy(items)})

    def parse_price(self, response):
        print(response.body.decode())
        items = response.meta["item"]

        items["book_price"] = json.loads(response.body.decode())[0]["m"]
        print(items)




