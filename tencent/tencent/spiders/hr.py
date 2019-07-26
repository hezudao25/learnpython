# -*- coding: utf-8 -*-
import scrapy
import json
from tencent.items import TencentItem
import math


class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['tencent.com']
    start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1563435686741&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex=1&pageSize=10&language=zh-cn&area=cn']

    def parse(self, response):
        res_list = json.loads(response.text)["Data"]
        # 数据量
        all_count = res_list["Count"]
        data_list = res_list["Posts"]

        for data in data_list:
            url = "https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1563500582931&postId={}&language=zh-cn".format(data["PostId"])

            yield scrapy.Request(url, callback=self.content, meta={'RecruitPostName': data["RecruitPostName"], 'LastUpdateTime': data["LastUpdateTime"], 'PostURL': url})
        # 统计总页数
        count = math.ceil(all_count / 10)

        if response.meta.get("pageindex") is None:
            pageindex = 2
        else:
            pageindex = int(response.meta["pageindex"]) + 1

        if pageindex <= count:
            next_url = "https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1563435686741&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn".format(pageindex)
            yield response.follow(next_url, callback=self.parse, meta={'pageindex': pageindex})



    def content(self, response):
        items = TencentItem()
        items["RecruitPostName"] = response.meta["RecruitPostName"]
        items["LastUpdateTime"] = response.meta["LastUpdateTime"]
        items["PostURL"] = response.meta["PostURL"]
        res_list = json.loads(response.text)
        items["Requirement"] = res_list["Data"]["Requirement"]
        yield items


