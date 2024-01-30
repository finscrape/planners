import scrapy


class CamdenSpider(scrapy.Spider):
    name = "camden"
    allowed_domains = ["a.com"]
    start_urls = ["https://a.com"]

    def parse(self, response):
        pass
