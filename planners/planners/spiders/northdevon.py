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

class NorthdevonSpider(scrapy.Spider):
    name = "northdevon"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []
    
    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
        for i in list(range(1,7032)):
            url = f"https://planning.northdevon.gov.uk/Search/Results/{i}"

            payload = {}
            headers = {
            'authority': 'planning.northdevon.gov.uk',
            'method': 'GET',
            'scheme': 'https',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'ASP.NET_SessionId=adbxabs00stqxg1ev0mwgn3j; __RequestVerificationToken=vg8CS-S4kg8aWdBXOqxupF2Zx4XZlKlVI-ih2Jo9WamGKXbSKrtIE7FsrziJLE7352rjvgchXD6fGY8SHcig-ZeAYQo9owJ9prLiwvL05Jk1'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            page = Selector(text=response.text)
            links = page.xpath("//a[@class='linkText']/@href").getall()
            self.listhref.extend(links)
        for i in self.listhref:
            abs_i = f'https://planning.northdevon.gov.uk{i}'
            yield scrapy.Request(url=abs_i,callback=self.parsedetails)

    def parsedetails(self,response):
        
        each = {}
        table_hd = response.xpath("//table[@class='summaryTbl table']/descendant::tr/td")
        for i in table_hd:
            first = i.xpath(".//text()").get()
            second = i.xpath(".//following-sibling::td/descendant::text()").getall()
            if second:
                second = ''.join(second)
                
                second = stripper(second)

                try:
                    fir = camel_case(first)

                    each[fir] = second
                except:
                    each[first] = second


        table_hd = response.xpath("//ul[@id='progressBarList']/li/descendant::tr[1]")
        for i in table_hd:
            first = i.xpath(".//descendant::text()").getall()
            first = ''.join(first)

            second = i.xpath(".//following-sibling::tr/descendant::text()").getall()
            second = ''.join(second)
            
            second = stripper(second)

            try:
                fir = camel_case(first)

                each[fir] = second
            except:
                each[first] = second


        yield each
        self.total.append(each)
        
            