# -*- coding: utf-8 -*-

import scrapy

class ParticipantItem (scrapy.Item):
    name = scrapy.Field()
    id = scrapy.Field()
    chance = scrapy.Field()

class HorseraceItem(scrapy.Item):

    def serialize_track(value):
        return str(value).split(' ', 1)[1]

    track = scrapy.Field(serializer=serialize_track)
    start = scrapy.Field()
    raceId = scrapy.Field()
    partList = scrapy.Field()
