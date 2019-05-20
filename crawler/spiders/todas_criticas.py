# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup

from crawler.cleaner import clean_synopysis
from crawler.items import MovieItem, MovieReview
from crawler.pipelines import MongoDBPipeline


class TodasCriticasSpider(scrapy.Spider):
    name = 'todas_criticas'
    allowed_domains = ["www.adorocinema.com"]
    start_urls = ['http://www.adorocinema.com/filmes/criticas-filmes/']

    def __init__(self, save=False):
        super().__init__()
        self.URL_BASE = "http://www.adorocinema.com"
        self.URL_TODAS_CRITICAS = "/filmes/criticas-filmes/"
        self.URL_CRITICA = "criticas-adorocinema/"
        self.URL_PAGE = "?page={}"
        self.db = MongoDBPipeline()
        self.save = save
        self.page = 0

    def parse(self, response):

        for div in response.xpath("//div[@class='card entity-card entity-card-list cf']"):
            movies = MovieItem()

            link = None
            if div.xpath(".//a[@class='meta-title-link']/@href").extract_first():
                link = self.URL_BASE + div.xpath(".//a[@class='meta-title-link']/@href").extract_first()

            movies['name'] = div.xpath(".//a[@class='meta-title-link']/text()").extract_first()
            movies['note'] = div.xpath(".//span[@class='stareval-note']/text()").extract_first()
            movies['link'] = link
            movies['synopsis'] = clean_synopysis(div.xpath(".//div[@class='synopsis']/div/text()").extract_first())

            if link:
                request = scrapy.Request(link + self.URL_CRITICA, callback=self.parse_review)
                request.meta['movies'] = movies
                yield request

        if response.xpath("//span[contains(text(),'Próxima')]").extract():
            self.page += 1
            yield scrapy.Request(self.URL_BASE + self.URL_TODAS_CRITICAS + self.URL_PAGE.format(self.page),
                                 callback=self.parse)

    def parse_review(self, response):
        movies_response = response.meta['movies']
        movies_review = MovieReview()
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
