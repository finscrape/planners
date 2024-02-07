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

class NorfolkSpider(scrapy.Spider):
    name = "norfolk"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []
    
    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
        for i in list(range(1,838)):
            
            url = f"https://eplanning.norfolk.gov.uk/Search/Results/{i}"

            payload = {}
            headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': '_gcl_au=1.1.2078431402.1704795704; _ga=GA1.1.335360936.1704795704; _hjFirstSeen=1; _hjIncludedInSessionSample_1236195=0; _hjSession_1236195=eyJpZCI6ImQ4YzVjMTYyLThiMTQtNGMwMS1iNzc3LWQzOWNkNDczNDI4NCIsImMiOjE3MDQ3OTU3MDQzNjMsInMiOjAsInIiOjAsInNiIjoxfQ==; _hjAbsoluteSessionInProgress=0; _hjSessionUser_1236195=eyJpZCI6ImZjYzVkYWIxLTA5NWQtNTBjMi04MjY3LWJmYmMyOGFhYTcxNSIsImNyZWF0ZWQiOjE3MDQ3OTU3MDQzNTksImV4aXN0aW5nIjp0cnVlfQ==; _uetsid=e2f94720aed811eebdad5bf93bcc396b; _uetvid=e2f9b210aed811ee9f6bfb3bb4070edc; ASP.NET_SessionId=lge4fiwj04gvopyvqxebp43a; __RequestVerificationToken=3w-2WlZJ0Z0DTp3q6XLc42F7LjS6tQl20RWfOdo3i-YvmMrQBFKnbGCkwCv0mZKmd2lfGtvsbJ3DdIJCGa_RQYU3tWaJtLa9KJ0Ap_AO70s1; _ga_S25NS40VD3=GS1.1.1704795703.1.1.1704795746.0.0.0'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            page = Selector(text=response.text)
            links = page.xpath("//dt[@class='underlineText']/a/@href").getall()
            self.listhref.extend(links)

        for i in self.listhref:
            abs_i = f'https://eplanning.norfolk.gov.uk{i}'
            yield scrapy.Request(url=abs_i,callback=self.parsedetails)

    def parsedetails(self,response):
        
        each = {}
        each['planningUrl'] = response.url
        rel_doc = []
        rd = response.xpath("//table[@summary='Consultations table']/descendant::tr")
        for i in rd[1:]:
            e_rel={}
            e_rel['consulteeName'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
            e_rel['dateSent'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            e_rel['consultationExpiryDate'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
            e_rel['dateReceived'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
            rel_doc.append(e_rel)


        table_hd = response.xpath("//dt")
        for i in table_hd:
            first = i.xpath(".//descendant::text()").get()
            second = i.xpath(".//following-sibling::dd/descendant::text()").get()
            if second:
                
                second = stripper(second)

                try:
                    fir = camel_case(first)

                    each[fir] = second
                except:
                    each[first] = second

        each['consulteeList'] = rel_doc
        yield each
        self.total.append(each)
        

