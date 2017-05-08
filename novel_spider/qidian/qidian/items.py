# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QidianItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field() 
    link = scrapy.Field()
    major_category = scrapy.Field() 
    intro = scrapy.Field()
    content = scrapy.Field()
    '''
    author = scrapy.Field()
    image = scrapy.Field()
    intro = scrapy.Field()
    progress = scrapy.Field()
    sign_status = scrapy.Field()
    pay_status = scrapy.Field()
    major_category = scrapy.Field()
    minor_category = scrapy.Field()
    total_text_count = scrapy.Field()
    total_click_count = scrapy.Field()
    vip_weekly_click_count = scrapy.Field()
    toal_recommend_count = scrapy.Field()
    weekly_recommend_count = scrapy.Field()
    monthly_pass_count = scrapy.Field()
    weekly_reward_count = scrapy.Field()
    '''
    #score = scrapy.Field()
    #evaluate_users = scrapy.Field()
