# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup

from crawler.cleaner import clean_synopysis
from crawler.items import movieItem, movieReview
from crawler.pipelines import MongoDBPipeline


class FilmesEmCartazSpider(scrapy.Spider):
    name = 'filmes_em_cartaz'
    allowed_domains = ["www.adorocinema.com"]
    start_urls = ['http://www.adorocinema.com/filmes/numero-cinemas/']

    def __init__(self, save=False):
        super().__init__()
        self.URL_BASE = "http://www.adorocinema.com"
        self.URL_SESSAO = "/filmes/numero-cinemas/"
        self.URL_TODAS_CRITICAS = "/filmes/criticas-filmes/"
        self.URL_CRITICA = "criticas-adorocinema/"
        self.URL_PAGE = "?page={}"
        self.db = MongoDBPipeline()
        self.save = save
        self.page = 0

    def parse(self, response):
        
        for div in response.xpath("//li[@class='mdl']"): 
            movies = movieItem()

            link = None
            if div.xpath("./div/div/h2/a/@href").extract_first():
                link = self.URL_BASE + div.xpath("./div/div/h2/a/@href").extract_first()

            movies['name'] = div.xpath("./div/div/h2/a/text()").extract_first() 
            movies['note'] = div.xpath("./div/div[3]/div[3]//span[@class='stareval-note']/text()").extract_first()
            movies['link'] = link
            movies['synopsis'] = clean_synopysis(div.xpath("./div//div[@class='synopsis']/div/text()").extract_first())

            if link:
                request = scrapy.Request(link + self.URL_CRITICA, callback=self.parse_review)
                request.meta['movies'] = movies
                yield request

        if response.xpath("//span[contains(text(),'Próxima')]").extract():
            self.page += 1
            yield scrapy.Request(self.URL_BASE + self.URL_SESSAO + self.URL_PAGE.format(self.page),
                                 callback=self.parse)

    def parse_review(self, response):
        movies_response = response.meta['movies']
        movies_review = movieReview()
        classification = response.xpath("//div[@class='big-note']/span[@class='light']/text()").extract()
        classification = "".join(classification).strip()
        movies_review['classification'] = classification

        for div in response.xpath("//div[@class='editorial-content cf']").extract():
            all_text = BeautifulSoup(div).text.split('\n')

            text = [t for t in all_text if "Alerta: O texto a seguir busca" not in t]

            review = " ".join(text)

            movies_review['review'] = review.strip()

        movies = {**movies_response, **movies_review}

        if self.save:
            yield self.db.process_item(movies)
        yield movies
