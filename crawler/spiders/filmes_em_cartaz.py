# -*- coding: utf-8 -*-
import scrapy
from collections import defaultdict


class FilmesEmCartazSpider(scrapy.Spider):
    name = 'filmes_em_cartaz'
    allowed_domains = ["www.adorocinema.com"]
    start_urls = ['http://www.adorocinema.com/filmes/numero-cinemas/']
    
    def __init__(self):
        self.URL_BASE = "http://www.adorocinema.com"

    def parse(self, response):
        movies = defaultdict(dict)
        for div in response.xpath("//li[@class='mdl']"): 
            movie = div.xpath("./div/div/h2/a/text()").extract_first() 
            note = div.xpath("./div/div[3]/div[3]//span[@class='stareval-note']/text()").extract_first()
            link = self.URL_BASE + div.xpath("./div/div/h2/a/@href").extract_first()

            movies[movie]['note'] = note
            movies[movie]['link'] = link
            
        yield movies