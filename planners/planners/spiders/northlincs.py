import scrapy
import requests

from typing import Iterable
import scrapy
from scrapy.http import Request
import requests
import requests
import json

from scrapy.selector import Selector

from re import sub

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

class NorthlincsSpider(scrapy.Spider):
    name = "northlincs"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []
    
    def start_requests(self) -> Iterable[Request]:
        for i in list(range(1,24)):
            yield scrapy.Request(url=f"https://apps.northlincs.gov.uk/?page={i}",method="GET")

    def parse(self,response):
    
        
        links = response.xpath("//div[@class='app-content']/a/@href").getall()
        for i in links:
            yield scrapy.Request(url=i,callback=self.parsedetails)

        
    def parsedetails(self,response):
        each = {}
        rel_doc = []
        
        app_com = []

        #getting related documents
        each['planningUrl'] = response.url
        rd = response.xpath("(//table[@class='display'][1])/tbody/tr")
        for i in rd:
            e_rel={}
            e_rel['documentType'] = stripper(i.xpath(".//td[1]/strong/text()").get())
            e_rel['description'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            e_rel['date'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
            e_rel['download'] = stripper(i.xpath(".//td[4]/descendant::a/@href").get())
            rel_doc.append(e_rel)
        
        rda = response.xpath("(//table[@class='display'][2])/tbody/tr")
        for i in rda:
            e_rel={}
            e_rel['type'] = stripper(i.xpath(".//td[1]/strong/text()").get())
            e_rel['name'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            e_rel['date'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
            e_rel['download'] = stripper(i.xpath(".//td[4]/descendant::a/@href").get())
            app_com.append(e_rel)
        
        all = response.xpath("//span[@class='col title']")

        for i in all:
            first = i.xpath(".//text()").get()
            if first:
                second = i.xpath(".//following-sibling::span/descendant::text()").getall()
                second = ''.join(second)
                
                second = second.replace('\r','').replace('\n','').replace('\t','').replace(":","").strip()
                

                try:
                    fir = camel_case(first)

                    each[fir] = second
                except:
                    each[first] = second

        each['relatedDocuments'] = rel_doc
        each['applicationComments'] = app_com


        yield each
        self.total.append(each)
        
