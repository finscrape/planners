from typing import Iterable
import scrapy
from scrapy.http import Request
import requests
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



class RibblevalleySpider(scrapy.Spider):
    name = "ribblevalley"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []
    
    def start_requests(self) -> Iterable[Request]:
        for i in list(range(1989,2025)):
            
            url = f"https://webportal.ribblevalley.gov.uk/planningApplication/search/results?location=&applicant=&developmentDescription=&decisionType=&decisionDate={i}&fromDay=&fromMonth=&fromYear=&toDay=&toMonth=&toYear=&advancedSearch=Search"
            yield scrapy.Request(url=url)
    def parse(self, response):
        
            links =response.xpath("//td/a[contains(@href,'/planningApplication/')]/@href").getall()
            for i in links:
                 abs_i = f'https://webportal.ribblevalley.gov.uk{i}'
                 yield scrapy.Request(url=abs_i,callback=self.parselinks)

            next_l = response.xpath("//a[contains(text(),'Next')]/@href").get()
            if next_l:
                 abs_next = f"https://webportal.ribblevalley.gov.uk{next_l}"
                 yield scrapy.Request(url=abs_next,callback=self.parse)

    def parselinks(self,response):
        each = {}
        each['planningUrl'] = response.url
        pl = response.xpath("//h1/text()").get()
        pl = pl.replace('Application','')
        each['planningApplication'] = pl
        table_hd = response.xpath("//tr")
        for i in table_hd:
            first = i.xpath(".//td[1]/descendant::text()").get()
            if first:
                if first == 'Attached files':
                    alla = i.xpath(".//td[2]/descendant::a").getall()
                    second = [f'https://webportal.ribblevalley.gov.uk{l}' for l in alla]
                    each['documents'] = second
                else:

                    second = i.xpath(".//td[2]/descendant::text()").getall()
                    second = ''.join(second)
                    
                    second = stripper(second)
                    

                    try:
                        fir = camel_case(first)

                        each[fir] = second
                    except:
                        each[first] = second

        yield each
        self.total.append(each)
        
              
