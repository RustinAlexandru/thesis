# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem

from funfly.models import Ninegag, Joke


class NineGagItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    source_url = scrapy.Field()
    imagevideo_path = scrapy.Field()
    points = scrapy.Field()


class NineGag(DjangoItem):
    django_model = Ninegag

class JokeItem(scrapy.Item):
    identifier = scrapy.Field()
    text = scrapy.Field()
    likes = scrapy.Field()
    dislikes = scrapy.Field()
    category = scrapy.Field()

class Joke(DjangoItem):
    django_model = Joke