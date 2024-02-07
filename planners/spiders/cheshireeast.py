import scrapy
from planners.util import dates_str4
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver

options = FirefoxOptions()
#options.add_argument("--headless")
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


class CheshireeastSpider(scrapy.Spider):
    name = "cheshireeast"
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
        #dispatcher.connect(self.spider_closed,signals.spider_closed)

    
    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
    
        self.driver.get("https://planning.cheshireeast.gov.uk/AdvancedSearch.aspx")
        
        #date picker
        sleep(10)

        try:
            self.driver.find_element('xpath',"//input[@id='ContentPlaceHolder1_optResultsTo_1']").click()
        except:
            try:
                self.driver.find_element('xpath',"//input[@id='ContentPlaceHolder1_optResultsTo_1']").click()
            except:
                pass
        
        try:
            self.driver.find_element('xpath',"//input[@value='Run Advanced Planning Search']").click()
        except:
            try:
                self.driver.find_element('xpath',"//input[@value='Run Advanced Planning Search']").click()
            except:
                pass
        
        sleep(120)

        try:
            self.driver.find_element('xpath',"//a[text()='Alternatively, view the results in paged format.']").click()
        except:
            try:
                self.driver.find_element('xpath',"//a[text()='Alternatively, view the results in paged format.']").click()
            except:
                pass
        
        sleep(60)
        pagex = self.driver.page_source
        html = Selector(text=pagex)
        links = html.xpath("//a[@class='planAppDetailsLink']/@href").getall()
        self.listhref.extend(links)
        print('Date search')
        length = len(self.listhref)
        print(f'{length} planning application')
        print(f'{length} planning application')
        print(f'{length} planning application')
        print(len(self.listhref))
        # x = 0
        # while True:
        #     x+=1
            
        #     try:
        #         self.driver.find_element("xpath","(//a[contains(text(),'Next ›')])[1]").click()
                
        #         page = self.driver.page_source
        #         html = Selector(text=page)

        #         check = html.xpath("(//a[contains(@disabled,'disabled')])[1]/text()").get()
        #         if check:
        #             break
        #         links = html.xpath("//ul[@class='filter-list']/li/a/@href").getall()
                
        #         self.listhref.extend(links)
        #         length = len(self.listhref)
        #         print(f'{length} planning application')
        #         print(f'{length} planning application')
        #         print(f'{length} planning application')
                
        #     except:
        #         break
