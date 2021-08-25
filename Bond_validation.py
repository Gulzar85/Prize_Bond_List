import scrapy


class BondValidationSpider(scrapy.Spider):
    name = 'Bond_validation'
    allowed_domains = ['savings.gov.pk']
    start_urls = ['http://savings.gov.pk/']

    def parse(self, response):
        pass
