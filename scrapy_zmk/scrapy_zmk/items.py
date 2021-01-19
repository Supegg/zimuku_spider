# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyZmkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    index = scrapy.Field()
    zh = scrapy.Field()
    en = scrapy.Field()
    suffix = scrapy.Field()
    sha1 = scrapy.Field()  # sha1 of url
    file_urls = scrapy.Field()
    files = scrapy.Field()
    