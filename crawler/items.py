# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class movieItem(Item):
    name = Field()
    link = Field()
    note = Field()
    synopsis = Field()
    classification = Field()
    review = Field()


class movieReview(Item):
    link = Field()
    synopsis = Field()
    classification = Field()
    review = Field()
