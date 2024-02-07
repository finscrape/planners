from typing import Any, Iterable
import scrapy
import scrapy
from planners.util import dates_str7
import requests
from scrapy.http import Request, Response
import scrapy

from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from shutil import which
from scrapy_selenium import SeleniumRequest
from time import sleep
from scrapy import Selector
from scrapy import signals
from pydispatch import dispatcher

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
global driver

option = webdriver.ChromeOptions()
option.add_argument('--headless=new')
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
                
    


# Define a function to convert a string to camel case
def camel_case(s):
    # Use regular expression substitution to replace underscores and hyphens with spaces,
    # then title case the string (capitalize the first letter of each word), and remove spaces
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    
    # Join the string, ensuring the first letter is lowercase
    return ''.join([s[0].lower(), s[1:]])


class WestlindseySpider(scrapy.Spider):
    name = "westLindsey"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    
    


    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []
        

    def start_requests(self):

        yield scrapy.Request(url='https://www.west-lindsey.gov.uk/planning-building-control/planning/view-search-planning-applications/search-planning-application-database')
    
    def parse(self,response):
        start = 0
        for d in dates_str7[0:-1]:
            start += 1
            fd = d
            nd = dates_str7[start]

            url = f"https://planning.west-lindsey.gov.uk/planning/results-iframe.asp?wardid=ALL&areaid=ALL&address_postcode=&address_street=&applicant_agent=&fromdate={fd}&todate={nd}&dates=application&stage=ALL"

            payload = {}
            headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'planning.west-lindsey.gov.uk',
            'Referer': 'https://planning.west-lindsey.gov.uk/planning/index-iframe.asp',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            sleep(1)
            print(f'From{fd} to {nd}----search')
            print(f'From{fd} to {nd}----search')
            print(f'From{fd} to {nd}----search')
            print(f'From{fd} to {nd}----search')

            html = response.text
            html_page = Selector(text=html)
            pl_links = html_page.xpath("//li[@class='result-item']/div/a[1]/@href").getall()
            
            for i in pl_links:
                abs_i = f'https://planning.west-lindsey.gov.uk/planning/{i}'
                yield scrapy.Request(url=abs_i,callback=self.next)
                sleep(2)

        
    def next(self,response):

        each = {}
        all = response.xpath("//div[@class='displayRow']/div")
        all1= response.xpath("//div[@class='displayRow']/div/text()").getall()
        for a in all:
            first = stripper(a.xpath(".//strong/text()").get())
            
            second = stripper(a.xpath(".//strong/following-sibling::text()").get())
            if second:
                pass
            else:
                second =""

            try:
                first = camel_case(first)

                each[first] = second
            except:
                each[first] = second

        doclink = response.xpath("//a[text()='View associated documents']/@href").get()
        if doclink:
            abs_doc = f'https://planning.west-lindsey.gov.uk/planning/{doclink}'
            yield scrapy.Request(url=abs_doc,callback=self.getdoc,meta={'each':each})
        else:    
            yield each
            self.total.append(each)
        

    def getdoc(self,response):
        each =response.meta['each']
        rd = response.xpath("//table/descendant::tr")
        if rd:  
            doc_doc =[] 
            for i in rd[1:]:
                e_rel={}
                e_rel['date'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                e_rel['documentType'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                e_rel['description'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                e_rel['additionalInformation'] = stripper(i.xpath(".//td[5]/descendant::text()").get())
                e_rel['documentLink'] = stripper(i.xpath(".//td[4]/descendant::a/@href").get())
                doc_doc.append(e_rel)
            
            each['documents'] = doc_doc
        yield each
        self.total.append(each)
        
            
