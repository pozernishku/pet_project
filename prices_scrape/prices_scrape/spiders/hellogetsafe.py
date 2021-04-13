import scrapy


class HellogetsafeSpider(scrapy.Spider):
    name = 'hellogetsafe'
    allowed_domains = ['hellogetsafe.com', 'www.hellogetsafe.com']
    start_urls = ['https://www.hellogetsafe.com/']

    def parse(self, response):
        pass
