import scrapy
from planners.util import dates_str
import scrapy
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


from re import sub
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
global driver

option = webdriver.ChromeOptions()
option.add_argument('--headless=new')
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


class SurreySpider(scrapy.Spider):
    name = "surrey"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []
        
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
        self.driver.maximize_window()

        self.drivera = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
        self.drivera.maximize_window()

        #dispatcher.connect(self.spider_closed,signals.spider_closed)

    
    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
        self.driver.get("https://planning.surreycc.gov.uk/Disclaimer?returnUrl=%2FSearch%2FResults%2F3")

        try:
            self.driver.find_element('xpath',"//input[@value='Accept']").click()
        except:
            try:
                self.driver.find_element('xpath',"//input[@value='Accept']").click()
            except:
                print('error with agree mutton')
        
        sleep(5)
        try:
            self.driver.find_element('xpath',"//input[@id='Search']").click()
        except:
            try:
                self.driver.find_element('xpath',"//input[@id='Search']").click()
            except:
                print('error with search mutton')
        sleep(1)
        pagex = self.driver.page_source
        html = Selector(text=pagex)
        links = html.xpath("//dd/a/@href").getall()
        self.listhref.extend(links)

        x = 0
        while True:
            x += 1
            try:
                self.driver.find_element("xpath","//a[@aria-label='Next Page.']").click()
                sleep(1)
                page = self.driver.page_source
                html = Selector(text=page)
                links = html.xpath("//dd/a/@href").getall()
                self.listhref.extend(links)
                print(f'page-----{x}')
                print(f'page-----{x}')
                print(f'page-----{x}')

                
            except:
                break
        
        for i in self.listhref:
            abs_i = f'https://planning.surreycc.gov.uk{i}'
            self.drivera.get(abs_i)

            try:
                self.drivera.find_element('xpath',"//input[@value='Accept']").click()
                sleep(2)
            except:
                try:
                    self.drivera.find_element('xpath',"//input[@value='Accept']").click()
                except:
                    print('error with agree mutton')
            
            

                
            pagey = self.drivera.page_source
            htmla = Selector(text=pagey)
                
            
            each = {}

            
            table_hd = htmla.xpath("//div[@class='col-md-3']")
            for i in table_hd:
                first = i.xpath(".//descendant::text()").get()
                if first:
                    first = stripper(first)
                second = i.xpath(".//following-sibling::*[1]/descendant::text()").get()
                if second:
                    
                    second = stripper(second)

                try:
                    fir = camel_case(first)

                    each[fir] = second
                except:
                    each[first] = second

            yield each
            self.total.append(each)
            
    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()
        
        spider.logger.info("Spider closed: %s", spider.name)
    

                            
