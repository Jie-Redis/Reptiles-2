# -*- coding: utf-8 -*-
import scrapy
import json
from Tencent.items import TencentItem

class HrSpider(scrapy.Spider):
    name = 'HR'
    allowed_domains = ['careers.tencent.com']
    # start_urls = ['http://careers.tencent.com/']
    one_url = "https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1604394635161&countryId=&cityId=&bgIds=&productId=&categoryId=40001001&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn"
    two_url = "https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1604394959298&postId={}&language=zh-cn"
    start_urls = [one_url.format(1)]

    def parse(self, response):
        # 获取的为前10页的数据
        for page in range(1, 11):
            url = self.one_url.format(page)
            # 发送请求 获取数据
            yield scrapy.Request(url=url, callback=self.parse_one)

    def parse_one(self, response):
        data = json.loads(response.text)
        # 获取岗位名字和职能
        # items = {}
        items = TencentItem()
        for jobs in data["Data"]["Posts"]:
            items["work_name"] = jobs.get("RecruitPostName")
            items["function"] = jobs.get("Responsibility")
            post_id = jobs.get("PostId")
            detail_url = self.two_url.format(post_id)
            yield scrapy.Request(url=detail_url, callback=self.parse_two, meta={"item": items})

    def parse_two(self, response):
        item = response.meta.get("item")
        detail_data = json.loads(response.text)
        item["name"] = detail_data["Data"]["RecruitPostName"]
        item["ablity"] = detail_data["Data"]["Responsibility"]
        yield item
