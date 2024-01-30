import scrapy

from typing import Iterable
import scrapy
from scrapy.http import Request
import requests
from time import sleep
from scrapy import Selector

from re import sub

# Define a function to convert a string to camel case
def camel_case(s):
    # Use regular expression substitution to replace underscores and hyphens with spaces,
    # then title case the string (capitalize the first letter of each word), and remove spaces
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    
    # Join the string, ensuring the first letter is lowercase
    return ''.join([s[0].lower(), s[1:]])

class WhitehorsedcSpider(scrapy.Spider):
    name = "whiteHorseDc"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(url="https://planning.walsall.gov.uk/swift/apas/run/WPHAPPCRITERIA")

    def parse(self, response):
        import requests

        for i in list(range(1946,2024)):
            for m in list(range(1,12)):
                m1 = m+1
                url = f"https://data.whitehorsedc.gov.uk/java/support/Main.jsp?MODULE=ApplicationCriteriaList&TYPE=Application&PARISH=ALL&AREA=&TXTSEARCH=&APP_TYPE=&APPTYPE=ALL&APP_STATUS=&SDAY=1&SMONTH={m}&SYEAR={i}&EDAY=1&EMONTH={m1}&EYEAR={i}&Submit=Search"

                    
                payload = {}
                headers = {
                'authority': 'data.whitehorsedc.gov.uk',
                'method': 'GET',
                'path': '/java/support/Main.jsp?MODULE=ApplicationCriteriaList&TYPE=Application&PARISH=ALL&AREA=&TXTSEARCH=&APP_TYPE=&APPTYPE=ALL&APP_STATUS=&SDAY=1&SMONTH=1&SYEAR=2021&EDAY=31&EMONTH=12&EYEAR=2023&Submit=Search',
                'scheme': 'https',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://data.whitehorsedc.gov.uk/java/support/Main.jsp?MODULE=ApplicationCriteria&TYPE=Application',
                'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
                }

                response = requests.request("GET", url, headers=headers, data=payload)

                page = response.text

                html = Selector(text=page)

                links = html.xpath("//div[@class='rowdiv']/div[@class='celldiv']/a/@href").getall()

                
                self.listhref.extend(links)

        for i in self.listhref:
            abs_i = f'https://data.whitehorsedc.gov.uk/java/support/{i}'
            yield scrapy.Request(url=abs_i,callback=self.getter)
    
    

    def getter(self,response):
        each  = {}
        box = response.xpath("//div[@class='rowdiv']/div[@class='leftcelldiv']")
        for i in box:
            title = i.xpath(".//text()").get()
            title = title.replace(":","")
            if 'Downloads' in title:
                pass
            else:
                data = i.xpath(".//following-sibling::div/descendant::text()").getall()
                if data:
                    dataa = ''.join(data)
                    dataa=dataa.replace('\r','').replace('\n','').replace('\t','')
                    dataa = dataa.strip()
                else:
                    dataa = ""


                fir = camel_case(title)

                each[fir] = dataa
        yield each
        self.total.append(each)
       
            