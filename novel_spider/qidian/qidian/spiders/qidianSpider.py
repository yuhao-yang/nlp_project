# -*- coding: UTF-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from qidian.items import QidianItem
from selenium import webdriver
import urllib
import re
import codecs


class Qidian(CrawlSpider):
    name='qidian'
    idx = 0
    browser = None
    dic = {}
    dic["都市"] = 0
    dic["科幻"] = 0
    dic["历史"] = 0
    dic["二次元"] = 0
    dic["玄幻"] = 0
    dic["游戏"] = 0
    dic["灵异"] = 0
    max_number = 3000
    num = 0

    def start_requests(self):
        #self.browser = webdriver.Chrome('d:/software/chromedriver.exe')
        urls = []
        #26047
        for i in range(1,5000):
            if self.num >= 21000:
                return 
            url = 'http://a.qidian.com/?page=%d' % i
            yield self.make_requests_from_url(url)


    def parse(self, response):
        if self.num >= 21000:
            return 
        selector = Selector(response)
        route_items = selector.xpath('//div[@class="book-mid-info"]')

        for route_item in route_items:            
            url = 'http:' + route_item.xpath('h4/a/@href').extract()[0]           
            yield Request(url,callback=self.parse_page)


    def parse_page(self, response):
        if self.num >= 21000:
            return 
        selector = Selector(response)
        
        item = QidianItem()
        item['url'] = response.url
		
        book_info = selector.xpath('//div[@class="book-info "]')        
        item['link'] = book_info.xpath('//a[@class="red-btn J-getJumpUrl "]/@href').extract()[0]
        item['name'] = book_info.xpath('h1/em//text()').extract()[0]        

        ast = selector.xpath('//div[@class="book-intro"]/p')[0]
        abcst = ast.xpath('text()').extract()
        abst = ""

        for d in abcst:
            abst += d

        item['intro'] = abst.replace('\n','')
        item['intro'] = abst.replace('\r','')
        item['intro'] = abst.replace('\t',' ')
        item['intro'] = abst.strip()
        
        tmp = book_info.xpath('p')
        book_tags = tmp[0]
        book_tags_hrefs = book_tags.xpath('a/text()')
        item['major_category'] = book_tags_hrefs[0].extract()
        
        na = item['name'].encode('utf-8')
        mc = item['major_category'].encode('utf-8')
        intr = item['intro'].encode('utf-8')
        li = item['link'].encode('utf-8')
        
        if li == "" or mc not in self.dic or self.dic[mc] >= self.max_number:
            return
        
        self.dic[mc] += 1
        self.num += 1

        yield Request("http:" + li,callback=self.parse_content)
        
        f0 = open('title2.txt','a')
        f1 = open('tag2.txt','a')
        f2 = open('abs2.txt','a')
        f3 = open('link2.txt','a')
        f0.write(str(na) + '\n')
        f1.write(str(mc) + '\n')
        f2.write(str(intr) + '\n')
        f3.write(str(li) + '\n')

        #print 'line82' + mc + '\n'
        #print 'line83 ' + str(self.dic)
        
        yield item
        
    def parse_content(self, response):
        selector = Selector(response)
        # item = QidianItem()
        a = response.xpath('//div[@class="read-content j_readContent"]/p')
        b = response.xpath('//div[@class="book-cover-wrap"]/h1/text()').extract()[0]
        #print 'line103 ' + str(type(a)) + '\n'
        t = ""
        for item in a:
            sen = item.xpath('text()').extract()[0]
            
            t = t + sen
            #print 'line107 ' + str(t.encode('utf-8'))
        '''    
        item['content'] = t
        item['content'].replace('\n','')
        item['content'].replace('\r','')
        item['content'].replace('\t',' ')
        item['content'].strip()

        if(item['content'] == ""):
            return
        '''
        t.replace('\n','')
        t.replace('\r','')
        t.replace('\t','')
        t.strip()

        with open('content2.txt','a') as f:
            f.write(str(b.encode('utf-8')) + ' ' + str(t.encode('utf-8')) + '\n')
        yield item



