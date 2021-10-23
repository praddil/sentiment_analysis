# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PostextractItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    headline = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    relevance = scrapy.Field()
    content = scrapy.Field()
    relevant_content = scrapy.Field()
