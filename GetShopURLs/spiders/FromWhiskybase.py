# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from GetShopURLs.items import Shop

def stripText(text):
    trans_table = {ord(c): None for c in u'\r\n\t'}
    return ' '.join(s.strip().translate(trans_table) for s in text)

# class Shop(object):
#   count = 0
#   def __init__(self, name, wb_url):
#     self.name = name
#     self.wb_url = wb_url
#     Shop.count += 1
#
#   # def display_count(self):
#   #   print "Total number of objects is %d" % Shop.count
#
#   def calculate_bmi(self):
#     return ( self.weight * 703 ) / ( self.height ** 2 )

class FromwhiskybaseSpider(scrapy.Spider):
    name = "FromWhiskybase"
    allowed_domains = ["whiskybase.com"]
    start_urls = ['https://www.whiskybase.com/explore/shop/']

    def parse(self, response):
        for sel in response.css(".compositor-gridrow"):
            l = ItemLoader(item=Shop(), selector=sel)
            l.add_css('name', '.info a:nth-child(1)::text')
            rel_shop_url = sel.css('.info a:nth-child(1)::attr(href)').extract_first()
            l.add_value('rel_shop_url', rel_shop_url)
            l.add_value('rel_prices_url', rel_shop_url[0:rel_shop_url.rfind('/')]+'/fetchshoplinks')
            print '-' * 20
            print l.load_item()
            # name = stripText(sel.css('a::text').extract())
            # url = sel.css('a::attr(href)').extract_first()
            # print '-' * 10
            # print name + ' - ' + url
            # # test = Shop("Test","http://wwww.google.com")

        # l = ItemLoader(item=Shop(), response=response)
        # l.add_css('name', '.info a:nth-child(1)::text')
        # l.add_css('url', '.info a:nth-child(1)::attr(href)')
        # print '-' * 20
        # print l.load_item()

        pass
