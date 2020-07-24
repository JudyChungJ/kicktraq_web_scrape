# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# status will be canceled or closed

import scrapy


class KicktraqItem(scrapy.Item):
    names = scrapy.Field()
    category = scrapy.Field()
    main_category = scrapy.Field() 
    proj_details = scrapy.Field()
    currency = scrapy.Field() #need to take first element translate with https://transferwise.com/gb/blog/world-currency-symbols might need to scrape
    # dates = scrapy.Field()
    # start_date = scrapy.Field()
    # deadline = scrapy.Field()
    goal = scrapy.Field()
    pledged = scrapy.Field()
    backers = scrapy.Field()
    status = scrapy.Field()
    description = scrapy.Field()
    # start_day = scrapy.Field()
    # year = scrapy.Field()

    # 'ID', 'name', 'category', 'main_category', 'currency', 'deadline',
    #    'goal', 'launched', 'pledged', 'state', 'backers', 'country',
    #    'usd pledged', 'usd_pledged_real', 'usd_goal_real'