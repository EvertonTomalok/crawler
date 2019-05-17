# -*- coding: utf-8 -*-
import scrapy
from crawler.items import movieItem
from crawler.pipelines import MongoDBPipeline
from crawler.cleaner import clean_synopysis


class FilmesEmCartazSpider(scrapy.Spider):
    name = 'filmes_em_cartaz'
    allowed_domains = ["www.adorocinema.com"]
    start_urls = ['http://www.adorocinema.com/filmes/numero-cinemas/']
    
    def __init__(self):
        self.URL_BASE = "http://www.adorocinema.com"
        self.db = MongoDBPipeline()

    def parse(self, response):
        
        for div in response.xpath("//li[@class='mdl']"): 
            movies = movieItem()
            movies['name'] = div.xpath("./div/div/h2/a/text()").extract_first() 
            movies['note'] = div.xpath("./div/div[3]/div[3]//span[@class='stareval-note']/text()").extract_first()
            movies['link'] = self.URL_BASE + div.xpath("./div/div/h2/a/@href").extract_first()
            movies['synopsis'] = clean_synopysis(div.xpath("./div//div[@class='synopsis']/div/text()").extract_first())
            
            yield self.db.process_item(movies)