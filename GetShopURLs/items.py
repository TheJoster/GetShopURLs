# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# from scrapy.loader.processors import Join, MapCompose, TakeFirst, Identity, Compose
# from w3lib.html import remove_tags

def stripText(text):
    trans_table = {ord(c): None for c in u'\t'}
    return ' '.join(s.strip().translate(trans_table) for s in text)

def filter_price(value):
    if value.isdigit():
        return value

class GetshopurlsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Shop(scrapy.Item):
    name = scrapy.Field()
    rel_shop_url = scrapy.Field()
    rel_prices_url = scrapy.Field()