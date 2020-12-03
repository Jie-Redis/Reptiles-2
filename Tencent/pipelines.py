# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from Tencent.items import TencentItem

class TencentPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,TencentItem):
            print(item)
        return item
