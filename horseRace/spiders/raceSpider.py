# -*- coding: utf-8 -*-

import scrapy
from horseRace.items import HorseraceItem, ParticipantItem


class raceSpider(scrapy.Spider):

    name = "raceSpider"
    allowed_domains = ["http://www.betbright.com/"]
    start_urls = [
        'http://www.betbright.com/horse-racing/today',
    ]
    def parse(self, response):

        for url in response.css("#selection_container_races_schedule .event_time::attr(href)").extract():
            yield scrapy.Request(url, callback=self.parse_dir_contents, dont_filter=True)

    def parse_dir_contents(self, response):

        item = HorseraceItem()
        horse = ParticipantItem()
        horses = []

        for selector in response.xpath(".//*/ul/li//ul[@class='horse']/li/ul[@class='horse-datafields']"):
            horse['id'] = selector.xpath("li[@class='horse-main-datafields-container']/"
                                         "ul/li/div[@class='horse-information-lefthand']/"
                                         "div[@class='cloth-number']/text()").extract_first()
            horse['name'] = selector.xpath("li[@class='horse-main-datafields-container']/"
                                           "ul/li/div[@class='horse-information-righthand']/"
                                           "div[@class='horse-information-name']/text()").extract_first()
            horse['chance'] = selector.xpath("li[4]/a[2]/text()").extract_first()
            horses.append(horse.copy())

        item['start'] = response.xpath(".//*/li[1]/div[2]/@data-start-date-time").extract()
        item['track'] = response.xpath(".//*/li[1]/div[1]/text()").extract_first()
        item['raceId'] = response.xpath(".//*/li[1]/div[2]/@data-event-id").extract()
        item['partList'] = horses

        yield item
