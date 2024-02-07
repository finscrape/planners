from typing import Iterable
import scrapy
from scrapy.http import Request
from planners.util import dates_str4
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver

options = FirefoxOptions()
options.add_argument("--headless")
from time import sleep
from scrapy import Selector
from scrapy import signals


from re import sub
global driver

from pydispatch import dispatcher

def stripper(second):
    if second:
        second = second.replace('\r','').replace('\n','').replace('\t','').replace(":","").strip()
    return second
                
    


# Define a function to convert a string to camel case
def camel_case(s):
    # Use regular expression substitution to replace underscores and hyphens with spaces,
    # then title case the string (capitalize the first letter of each word), and remove spaces
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    
    # Join the string, ensuring the first letter is lowercase
    return ''.join([s[0].lower(), s[1:]])


class CopelandSpider(scrapy.Spider):
    name = "copeland"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(url="https://www.copeland.gov.uk/planning/application-search?page=0")

    def parse(self, response):
        links = response.xpath("//td/a/@href").getall()
        for i in links:
            abs_i = f'https://www.copeland.gov.uk{i}'
            yield scrapy.Request(url=abs_i,callback=self.parsedetails)


        next = response.xpath("//a[@title='Go to next page']/@href").get()
        if next:
            abs_next = f"https://www.copeland.gov.uk{next}"
            yield scrapy.Request(url=abs_next,callback=self.parse)

    def parsedetails(self,response):
        each = {}
        each['planningUrl'] = response.url
        num = response.xpath("//h1[@id='page-title']/text()").get()
        each['planningApplication'] = num.replace('Application','')

        table_hd = response.xpath("//div[@class='field-label']")
        for i in table_hd:

            first = i.xpath(".//descendant::text()").get()
            if first and first != "  ":
                first = stripper(first)
                second = i.xpath(".//following-sibling::div[1]/descendant::text()").getall()
                if second:
                    second = ''.join(second)
                    second = stripper(second)
                else:
                    second = ""
                try:
                    fir = camel_case(first)

                    each[fir] = second
                except:
                    each[first] = second

        nei_doc = []
        rd = response.xpath("//span[@class='file']/a")
        for i in rd:
            e_rel={}
            e_rel['fileName'] = stripper(i.xpath(".//@title").get())
            e_rel['link'] = stripper(i.xpath(".//@href").get())
            nei_doc.append(e_rel)
        each['documents'] = nei_doc

        yield each