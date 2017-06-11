# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from GetShopURLs.items import Shop, Distillery, Brand, Bottler, Whisky

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.utils.response import open_in_browser
from GetShopURLs.basevariables import distilleries

import re # RegEx

def stripText(text):
    trans_table = {ord(c): None for c in u'\r\n\t'}
    return ' '.join(s.strip().translate(trans_table) for s in text)

def parse_table(self, response, selector, cName):
    #parseClass = globals()[cName]
    #for sel in response.css(".compositor-gridrow"):
    l = ItemLoader(item=cName(), selector=selector)

    if type(l.item) is Shop:
        l.add_value('type',type(l.item).__name__)
        l.add_css('name', '.info a:nth-child(1)::text')
        rel_shop_url = selector.css('.info a:nth-child(1)::attr(href)').extract_first()
        l.add_value('rel_shop_url', rel_shop_url)
        rel_prices_url = rel_shop_url[0:rel_shop_url.rfind('/')]
        l.add_value('rel_prices_url', rel_prices_url+'/fetchshoplinks')
        id = rel_prices_url[rel_prices_url.rfind('/')+1:]
        l.add_value('id', id)

    elif type(l.item) is Whisky:
        if selector.css('a.clickable::text').extract_first() == None:
            return None
        l.add_value('type',type(l.item).__name__)
        l.add_css('id', 'td:nth-child(2)::text')
        #l.add_css('name', 'a.clickable *::text')
        test = stripText(selector.css('a.clickable *::text').extract())
        l.add_value('name', test.strip())
        l.add_css('stated_age', 'td:nth-child(4)::text')
        l.add_css('strength', 'td:nth-child(5)::text')
        l.add_css('size', 'td:nth-child(6)::text')
        l.add_css('bottled', 'td:nth-child(7)::text')
        l.add_css('casknumber', 'td:nth-child(8)::text')
        l.add_css('barcode', 'td:nth-child(9)::text')
        l.add_css('rating', 'td:nth-child(10)::text')
        l.add_css('country', 'img.countryflag::attr(title)') #'td:nth-child(11)::text')
        l.add_css('region', 'td:nth-child(12)::text')
        l.add_css('versions', 'td:nth-child(13)::text')
        l.add_css('shoplinks', 'span.shoplink-av::attr(title)') #'td:nth-child(14)::text')
        l.add_css('detailslink','a.clickable::attr(href)')

    else:
        if selector.css('.clickable a::text').extract_first() == None:
            return None
        l.add_value('type',type(l.item).__name__)
        id = selector.css('.clickable a::attr(href)').extract_first()
        id = id[0:selector.css('.clickable a::attr(href)').extract_first().rfind('/')]
        id = id[id.rfind('/')+1:]
        l.add_value('id', id)
        l.add_css('name', '.clickable a::text')
        l.add_css('country', '.clickable+ td.data::text')
        l.add_css('number_of_whiskies', 'td:nth-child(3)::text')

    return l.load_item()

class FromwhiskybaseSpider(scrapy.Spider):
    name = "FromWhiskybase"
    allowed_domains = ['whiskybase.com']
    start_urls = [
    #   'https://www.whiskybase.com/explore/shop/',
       'https://www.whiskybase.com/whiskies/brands',
    #   'https://www.whiskybase.com/whiskies/distilleries',
    #   'https://www.whiskybase.com/whiskies/bottlers',
    #   'https://www.whiskybase.com/search?style=table&bottler=&brandname=&vintage_year=&bottle_date_year=&itemsforsale=&rating=&h=whisky.id,whisky.age,whisky.strength,whisky.bottle_size,whisky.bottle_date_year,whisky.cask_number,whisky.barcode,whisky.rating,user.country,generic.region,whisky.otherreleases,whisky.shoplinks,style&q=ardbeg',
    ]
    
    #start_urls = ['http://www.toele.nl']

    #rules = (
    #    Rule(LinkExtractor(allow='www\.whiskybase\.com\/explore\/shop'),
    #        'parse_category', follow=True, callback=parse
    #    ),
    #)


    def parse(self, response):
        #resultArray = []
        
        if '.com/explore/shop/' in response.url:
            for sel in response.css(".compositor-gridrow"):
                parsed_class = parse_table(self,response, sel, Shop)
                if parsed_class == None: continue #return
                yield parsed_class

                '''
                #l = ItemLoader(item=Shop(), selector=sel)
                #l.add_css('name', '.info a:nth-child(1)::text')

                #rel_shop_url = sel.css('.info a:nth-child(1)::attr(href)').extract_first()
                #l.add_value('rel_shop_url', rel_shop_url)

                #rel_prices_url = rel_shop_url[0:rel_shop_url.rfind('/')]
                #l.add_value('rel_prices_url', rel_prices_url+'/fetchshoplinks')

                #id = rel_prices_url[rel_prices_url.rfind('/')+1:]
                #l.add_value('id', id)
                #yield l.load_item()
                '''
        elif '.com/whiskies/brands' in response.url:
            for sel in response.css('tr'): #('.clickable+ .data , .clickable'):
                parsed_class = parse_table(self,response, sel, Brand)
                if parsed_class == None: continue #return
                yield parsed_class
                
                #if (parsed_class['name'][0].find('Mountain') > 0) or (parsed_class['name'][0].find('%') > 0):
                #    pass

                query = re.sub(r'[^a-zA-Z0-9 ]', '', parsed_class['name'][0])
                query = query.replace(' ','+')
                search4brands_url = 'https://www.whiskybase.com/search?style=table&bottler=&brandname=&vintage_year=&bottle_date_year=&itemsforsale=&rating=&h=whisky.id,whisky.age,whisky.strength,whisky.bottle_size,whisky.bottle_date_year,whisky.cask_number,whisky.barcode,whisky.rating,user.country,generic.region,whisky.otherreleases,whisky.shoplinks,style&q=' + parsed_class['name'][0].replace(' ','+')
                
                #yield scrapy.Request(search4brands_url, callback = self.parse)

                '''
                #if sel.css('.clickable a::text').extract_first() == None:
                #   continue
                #distillery = ItemLoader(item=Brand(), selector=sel)
                #distillery.add_value('type','Brand')
                #id = sel.css('.clickable a::attr(href)').extract_first()
                #id = id[0:sel.css('.clickable a::attr(href)').extract_first().rfind('/')]
                #id = id[id.rfind('/')+1:]
                #distillery.add_value('id', id)
                #distillery.add_css('name', '.clickable a::text')
                #distillery.add_css('country', '.clickable+ td.data::text')
                #distillery.add_css('number_of_whiskies', 'td:nth-child(3)::text')
                #yield distillery.load_item()

            #brand = ItemLoader(item=Brand())
            #brand.add_value('type','Brand')
            #for sel in response.css('.clickable+ .data , .clickable'):
            #    brand.selector = sel
            #    brand.add_css('name', 'a::text')
            #    brand.add_css('country', 'td::text')
            #yield brand.load_item()
            # It is possible to yield more than once
            #yield Distillery(name = sel.css('a::text').extract())
            '''
        elif '.com/whiskies/distilleries' in response.url:
            for sel in response.css('tr'): #('.clickable+ .data , .clickable'):
                parsed_class = parse_table(self,response, sel, Distillery)
                if parsed_class == None: continue #return
                yield parsed_class
                '''
                #if sel.css('.clickable a::text').extract_first() == None:
                #   continue
                #distillery = ItemLoader(item=Distillery(), selector=sel)
                #distillery.add_value('type','Distillery')
                #id = sel.css('.clickable a::attr(href)').extract_first()
                #id = id[0:sel.css('.clickable a::attr(href)').extract_first().rfind('/')]
                #id = id[id.rfind('/')+1:]
                #distillery.add_value('id', id)
                #distillery.add_css('name', '.clickable a::text')
                #distillery.add_css('country', '.clickable+ td.data::text')
                #distillery.add_css('number_of_whiskies', 'td:nth-child(3)::text')
                #yield distillery.load_item()
                '''
        elif '.com/whiskies/bottlers' in response.url:
            for sel in response.css('tr'): #('.clickable+ .data , .clickable'):
                parsed_class = parse_table(self,response, sel, Bottler)
                if parsed_class == None: continue #return
                yield parsed_class

        elif '.com/search' in response.url:
            for sel in response.css('tr'):
                parsed_class = parse_table(self,response, sel, Whisky)
                if parsed_class == None: continue #return
                yield parsed_class

        else:
            for sel in response.css('b'):
                self.logger.debug('Found following text: %s' % sel.extract())
                #print "Found following text: " + sel.extract()
                #if any(word in sel.extract().upper() for word in distilleries):
                words = [word for word in distilleries if word in sel.extract().upper()]
                if words:
                    self.logger.debug('Distillery found: %s' % words)
                    l = Shop(name = words[0], id = 1)
                    yield l

                    #l = ItemLoader(item=Distillery())
                    #l.add_value('name', 'test')
                    #l.add_value('name', 1)
                    #yield l.load_item()
        
        # Handy finds in Python
        #         
        # open_in_browser(response) # Open response in browser
        # ['http://example.com/superurl/top/page-%d/' % i for i in xrange(55)] # Generate numbers after string
        
        # Example which parses two fields using: zip()
        # hxs = HtmlXPathSelector(response)
        # for eponimia, address in zip(hxs.select("//a[@itemprop='name']/text()").extract(),
        #                                hxs.select("//div[@class='results_address_class']/text()").extract()):
        #    vriskoit = VriskoItem()
        #    vriskoit['eponimia'] = eponimia.encode('utf-8')
        #    vriskoit['address'] = address.encode('utf-8')
        #    yield vriskoit

        pass

