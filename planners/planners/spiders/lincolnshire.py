import scrapy
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from shutil import which
from scrapy_selenium import SeleniumRequest
from scrapy import signals
from typing import Iterable
import scrapy
from scrapy.http import Request
import requests
import requests
import json

from scrapy.selector import Selector

from re import sub
from re import sub
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
global driver

option = webdriver.ChromeOptions()
option.add_argument('--headless=new')

def stripper(second):
    if second:
        second = second.replace('\r','').replace('\n','').replace('\t','').replace(":","").strip()
    return second
                
    
    

from pydispatch import dispatcher
# Define a function to convert a string to camel case
def camel_case(s):
    # Use regular expression substitution to replace underscores and hyphens with spaces,
    # then title case the string (capitalize the first letter of each word), and remove spaces
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    
    # Join the string, ensuring the first letter is lowercase
    return ''.join([s[0].lower(), s[1:]])


class LincolnshireSpider(scrapy.Spider):
    name = "lincolnshire"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []
        dispatcher.connect(self.spider_closed,signals.spider_closed)

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)

    
    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
        import requests
        for i in list(range(1,290)):
            print(f'page{i}')
            url = f"https://lincolnshire.planning-register.co.uk/Search/Results/{i}"

            payload = {}
            headers = {
            'authority': 'lincolnshire.planning-register.co.uk',
            'method': 'GET',
            'scheme': 'https',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': '_ga_YVDE3WDGF1=GS1.1.1703252358.2.1.1703257081.0.0.0; nmstat=23a43c5d-43a5-f2d7-f1e7-4c263e631c05; _ga=GA1.3.433435929.1703239909; _ga_XW7G8JKYH3=GS1.3.1703925673.3.1.1703925693.0.0.0; ASP.NET_SessionId=e44ztobtr0us4lorj2g5i3hf; __RequestVerificationToken=PVbZtbt3ZWOUtMZKSt0D3YQ5x9h6DxP1gE5JrQXvpbG4ls0bItoVP9A8TV3znpaitAL11KOB92i1NiJNF1kLjFse4q4rLfGv6Yg39_BfD3o1; AcceptedDisclaimer=11/01/2024 20:04:30'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            page = Selector(text=response.text)
            links = page.xpath("//dt/a/@href").getall()
            self.listhref.extend(links)
            print(i)
            print(i)
            print(i)
            print(i)
            print(i)
    
        for i in self.listhref:
                abs_i = f'https://lincolnshire.planning-register.co.uk{i}'
                yield scrapy.Request(url=abs_i,callback=self.parsedetails,meta={'u':abs_i})

    def parsedetails(self,response):
        self.driver.maximize_window()

        u = response.meta['u']
        self.driver.get(u)

        try:
            self.driver.find_element('xpath',"//input[@value='Agree']").click()
        except:
            try:
               self.driver.find_element('xpath',"//input[@value='Agree']").click()
            except:
                pass


        responsee = self.driver.page_source
        
        
        page = Selector(text=responsee)
        each = {}
        each['planningUrl'] = u

        rel_doc = []
        rd = page.xpath("//h3[text()='Consultee List']/following-sibling::table[1]/descendant::tr")
        for i in rd[1:]:
            e_rel={}
            e_rel['consulteeName'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
            e_rel['dateLetterSent'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            e_rel['consultationExpiryDate'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
            e_rel['dateReceived'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
            rel_doc.append(e_rel)

        nei_doc = []
        rd = page.xpath("//h3[text()='Consultee List']/following-sibling::table[2]/descendant::tr")
        for i in rd[1:]:
            e_rel={}
            e_rel['address'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
            e_rel['dateLetterSent'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            e_rel['consultationExpiryDate'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
            e_rel['dateReceived'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
            nei_doc.append(e_rel)

        table_hd = page.xpath("//dt")
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
        each['neighborList'] = nei_doc
        yield each
        self.total.append(each)
        

    def spider_closed(self, spider):
        self.driver.close()
        spider.logger.info("Spider closed: %s", spider.name)
    

