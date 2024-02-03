import scrapy


class BarrowbcSpider(scrapy.Spider):
    name = "barrowbc"
    allowed_domains = ["a.com"]
    start_urls = ["https://a.com"]

    def parse(self, response):
        pass
