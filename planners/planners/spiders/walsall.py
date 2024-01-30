from typing import Iterable
import scrapy
from scrapy.http import Request
import requests
from time import sleep
from scrapy import Selector
from planners.util import dates_str8
from re import sub

# Define a function to convert a string to camel case
def camel_case(s):
    # Use regular expression substitution to replace underscores and hyphens with spaces,
    # then title case the string (capitalize the first letter of each word), and remove spaces
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    
    # Join the string, ensuring the first letter is lowercase
    return ''.join([s[0].lower(), s[1:]])

def stripper(second):
    if second:
        second = second.replace('\r','').replace('\n','').replace('\t','').replace(":","").strip()
    return second
                
    


class WalsallSpider(scrapy.Spider):
    name = "walsall"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(url="https://www.ebay.com")

    def parse(self, response):
        
        start = 0
        for d in dates_str8[0:-1]:
            start += 1
            fd = d
            nd = dates_str8[start]
            
            url = "https://planning.walsall.gov.uk/swift/apas/run/WPHAPPCRITERIA"
            
            payload = f"APNID.MAINBODY.WPACIS.1=&JUSTLOCATION.MAINBODY.WPACIS.1=&JUSTDEVDESC.MAINBODY.WPACIS.1=&REGFROMDATE.MAINBODY.WPACIS.1=&REGTODATE.MAINBODY.WPACIS.1=&DECFROMDATE.MAINBODY.WPACIS.1={fd}&DECTODATE.MAINBODY.WPACIS.1={nd}&APELDGDATFROM.MAINBODY.WPACIS.1=&APELDGDATTO.MAINBODY.WPACIS.1=&APEDECDATFROM.MAINBODY.WPACIS.1=&APEDECDATTO.MAINBODY.WPACIS.1=&WARD.MAINBODY.WPACIS.1=&SEARCHBUTTON.MAINBODY.WPACIS.1=Search"

            print(payload)
            headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Length": "425",
            "Content-Type": "application/x-www-form-urlencoded"
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            page = response.text

            html = Selector(text=page)

            links = html.xpath("//div[@class='apas_form_text']/p[2]/a/@href").getall()
            if links:
                print(f'{fd}----planning applications')
                print(f'{fd}----planning applications')
                print(f'{fd}----planning applications')
                print(f'{fd}----planning applications')
                print(f'{fd}----planning applications')
                link1 = links[0]
                link1 = link1.replace("StartIndex=11","StartIndex=1")
                self.listhref.append(link1)

                self.listhref.extend(links)

        for i in self.listhref:
            abs_i = f'https://planning.walsall.gov.uk/swift/apas/run/{i}'
            yield scrapy.Request(url=abs_i,callback=self.get)
    
    def get(self,response):
        links = response.xpath("//td[@class='apas_tblContent']/a/@href").getall()
        for i in links:
            abs_i = f'https://planning.walsall.gov.uk/swift/apas/run/{i}'
            yield scrapy.Request(url=abs_i,callback=self.getter)
    

    def getter(self,response):
        each  = {}
        each['planningUrl'] = response.url
        box = response.xpath("//div[@class='fieldset_divdata']/span[@class='apas']")
        if box:
            for i in box:
                title = i.xpath(".//text()").get()
                title = title.replace(":","")

                data = i.xpath(".//following-sibling::*[@class='fieldset_data']/descendant::text()").getall()
                if data:
                    dataa = ''.join(data)
                    dataa=dataa.replace('\r','').replace('\n','').replace('\t','')
                    dataa = dataa.strip()
                else:
                    dataa = ""


                fir = camel_case(title)

                each[fir] = dataa

        
        nei_doc = []
        rd = response.xpath("//table[@id='tableConsultees']/descendant::tr")
        for i in rd[1:]:
            e_rel={}
            e_rel['name'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
            e_rel['description'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            nei_doc.append(e_rel)

        if nei_doc:
            each['consultees'] = nei_doc

        neib_doc = []
        rd = response.xpath("//table[@id='tableNeighbours']/descendant::tr")
        for i in rd[1:]:
            e_rel={}
            e_rel['address'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
            e_rel['lastLetterDate'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            e_rel['targetResponseDate'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            neib_doc.append(e_rel)
        if neib_doc:
            each['neighbours'] = neib_doc


        yield each
        self.total.append(each)
       