# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field

class DetoxmarketItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    number = Field()    
    name = Field()
    tag = Field()
    feature = Field()
    rating = Field()
    price = Field()
    description = Field()
    ingredients = Field()
    howToUse = Field()
    otherDetail = Field()
    scrapedDate = Field()
    imageSrc = Field()
    imageList = Field()
    pass
