# -*- coding: utf-8 -*-
import scrapy
import csv
from scrapy.http import Request
from time import sleep

class YoutubeSpider(scrapy.Spider):
    name = 'youtube'
    allowed_domains = ['www.youtube.com']
    start_urls = ['http://www.youtube.com/']
    handle_httpstatus_list = [503]

    def parse(self, response):

        with open('Brands.txt', 'rt', encoding='UTF-8') as data:
            for link in data:
                link = "Автошины+"+link
                url = "https://www.youtube.com/results?search_query={}".format(link)
                name = link.replace('+',' ')
                yield Request(url, meta={'name':name}, callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        if response.status == 503:
            sleep(200)
            yield response.follow(response.url, self.parse_page)
        urls = []
        links = response.xpath('//a[contains(@href, "watch?v=")]/@href').extract()
        links = links[0:6]
        for link in links:
            urls.append("https://www.youtube.com"+link)
        name = response.meta['name']

        yield{
            'name':name,
            'link1':urls[0],
            'link2':urls[2],
            'link3':urls[4],
        }