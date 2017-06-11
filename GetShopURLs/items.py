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

def serialize_name(value):
    return str(value)

class GetshopurlsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Base(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    #name = scrapy.Field(serializer = serialize_name)
    type = scrapy.Field()
    
class Distillery(Base):
    country = scrapy.Field()
    number_of_whiskies = scrapy.Field()
    #type = 'Distillery'

class Brand(Distillery):    
    pass
    #type = 'Brand'

class Bottler(Distillery):
    pass
    #type = 'Bottler'

class Whisky(Base):
    stated_age = scrapy.Field()
    strength = scrapy.Field()
    size = scrapy.Field()
    bottled = scrapy.Field()
    casknumber = scrapy.Field()
    barcode = scrapy.Field()
    rating = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    versions = scrapy.Field()
    shoplinks = scrapy.Field()
    detailslink = scrapy.Field()

class Shop(Base):
    rel_shop_url = scrapy.Field()
    rel_prices_url = scrapy.Field()
    shop_url = scrapy.Field()
    #type = 'Shop'