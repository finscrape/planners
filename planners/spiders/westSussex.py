from typing import Iterable
import scrapy

import scrapy
from scrapy.http import Request

import scrapy
from planners.util import dates_str5
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




class WestsussexSpider(scrapy.Spider):
    name = "westSussex"
    # allowed_domains = ['a.com']
    # start_urls = ['http://a.com/']

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = 0
        self.total = []
        self.driver = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
        self.driver.maximize_window()

        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def start_requests(self):
        yield scrapy.Request(url='https://www.ebay.com',callback=self.parse)
                
    def parse(self,response):

        self.driver.get("https://westsussex.planning-register.co.uk/Search/Advanced")

        try:
            searchPl = self.driver.find_element('xpath',"//input[@value='Search']")
            self.driver.execute_script("arguments[0].scrollIntoView();", searchPl)
            self.driver.execute_script("arguments[0].click();", searchPl)
        except:
            pass    
        sleep(5)
        #get planning apllications link
        page = self.driver.page_source
        html = Selector(text=page)
        li = html.xpath("//a[contains(@href,'/Planning/Display')]/@href").getall()
        self.listhref.extend(li)

        last = html.xpath("//li[contains(a/text(),'Next')]/preceding-sibling::li")
        if last:
            lastt = last[-1]
            last_num = lastt.xpath(".//a/text()").get()
            
            num = 1
            while num < int(last_num):
                try:
                    self.driver.find_element('xpath',"//li[contains(a/text(),'Next')]/a").click()
                    sleep(2)
                    page = self.driver.page_source
                    html = Selector(text=page)
                    li = html.xpath("//a[contains(@href,'/Planning/Display')]/@href").getall()
                    self.listhref.extend(li)
                    print(f'{num}- planning applications')
                    print(f'{num}- planning applications')
                    print(f'{num}- planning applications')
                    print(f'{num}- planning applications')
                    num+=1
                except:
                    break

            for c in self.listhref:
                
                abs_i = f'https://westsussex.planning-register.co.uk{c}'
                yield scrapy.Request(url=abs_i,callback=self.final,dont_filter=True)

    def final(self,response):     
        each = {}
        each['planningUrl'] = response.url
        detail = response.xpath("//ul[@class='detailsList']/li")

        for i in detail:
            table_hd = i.xpath(".//label/descendant::text()").get()
            if table_hd:
                table_hd = stripper(table_hd)
                second = i.xpath(".//label/following-sibling::div[1]/descendant::text()").getall()
                second = ''.join(second)
                second = stripper(second)

                fir = camel_case(table_hd)

                each[fir] = second


        nei_doc = []
        rd = response.xpath("//table[@class='table sortable document-list']/descendant::tr/td[2]")
        for i in rd[1:]:
            e_rel={}
            e_rel['fileName'] = stripper(i.xpath(".//a/descendant::text()").get())
            e_rel['description'] = stripper(i.xpath(".//following-sibling::td[1]/descendant::text()").get())
            alink =  stripper(i.xpath(".//descendant::a/@href").get())
            if alink:
                e_rel['download'] =  'https://westsussex.planning-register.co.uk/' + alink
                e_rel['dateUploaded'] = stripper(i.xpath(".//following-sibling::td[2]/descendant::text()").get())
                nei_doc.append(e_rel)
        if nei_doc:
            each['documents'] = nei_doc

         
        yield each
        self.total.append(each)
        

    def spider_closed(self, spider):
        self.driver.close()
        spider.logger.info("Spider closed: %s", spider.name)
        
        