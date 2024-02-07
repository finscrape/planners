from typing import Iterable
import scrapy
from scrapy.http import Request

import scrapy
from planners.util import dates_str9
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



class StratfordSpider(scrapy.Spider):
    name = "stratford"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = 0
        self.total = []
        self.driver = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
        self.driver.maximize_window()

        self.drivera = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
        self.drivera.maximize_window()
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    
    


    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(url="https://apps.stratford.gov.uk/eplanning/AdvancedSearch.aspx")
    def parse(self,response):
        start=0
        for d in dates_str9[0:-1]:
                    
            start += 1
            fd = d
            nd = dates_str9[start]
            url = f'https://apps.stratford.gov.uk/eplanning/AppSearchResult.aspx?searchby=advanced&appnumber=&apptype=&status=&decision=&ward=&parish=&agent=&datereceivedfrom={fd}&datereceivedto={nd}&datevalidatedfrom=&datevalidatedto=&dateissuedfrom=&dateissuedto=&appealstatus=&appealdecision=&appealstartdatestart=&appealstartdateend=&appealdecisiondatestart=&appealdecisiondateend='
            self.driver.get(url)
            sleep(1)
            page = self.driver.page_source
            html = Selector(text=page)

            links = html.xpath("//tr/td/a/@href").getall()
            if links:
                self.listhref.extend(links)
                l = len(self.listhref)
                print(f'{l} planning apps')
                print(f'{l} planning apps')
                print(f'{l} planning apps')
                print(f'{l} planning apps')
                print(f'{l} planning apps')

                    
                try:
                    num =0
                    nextPl = self.driver.find_elements('xpath',"//div[@class='AspNet-GridView-Pagination AspNet-GridView-Bottom']/a")
                    for x in nextPl:
                        
                        nextli = self.driver.find_elements('xpath',"//div[@class='AspNet-GridView-Pagination AspNet-GridView-Bottom']/a")
                        y = nextli[num]
                        num += 1
                        print(f'{num}- planning applications')
                        print(num)
                        print(num)
                        self.driver.execute_script("arguments[0].scrollIntoView();", y)
                        self.driver.execute_script("arguments[0].click();", y)
                        sleep(2)
                        
                        page = self.driver.page_source
                        html = Selector(text=page)

                        links = html.xpath("//tr/td/a/@href").getall()
                        self.listhref.extend(links)
                        
                except:
                    pass    
            
            
        for i in self.listhref:
            abs_i = f'https://apps.stratford.gov.uk/eplanning/{i}'
            self.drivera.get(abs_i)
            
            page = self.drivera.page_source
            html = Selector(text=page)
            
            
            
            each = {}
            each['planningUrl'] = self.drivera.current_url
            box = html.xpath("(//div[@class='left'] | //div[contains(@class,'column')][1] | //div[contains(@class,'column')][3])")
            for i in box:
                table_hd = i.xpath(".//descendant::text()").get()
                if table_hd:
                
                    second = i.xpath(".//following-sibling::div[1]/descendant::text()").getall()
                    if second:
                        allsecond = ''.join(second)
                        allsecond = stripper(allsecond)
                    else:
                        allsecond = ""
                    try:
                        fir = camel_case(table_hd)

                        each[fir] = allsecond
                    except:
                        each[table_hd] = allsecond

            
                
            yield each
            self.total.append(each)
            
    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()

        spider.logger.info("Spider closed: %s", spider.name)
    