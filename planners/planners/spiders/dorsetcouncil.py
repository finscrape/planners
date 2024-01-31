import scrapy
from planners.util import dates_strx
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


class DorsetcouncilSpider(scrapy.Spider):
    name = "dorsetcouncil"
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

    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
            self.driver.get("https://planning.dorsetcouncil.gov.uk/disclaimer.aspx?returnURL=%2fadvsearch.aspx%3fAspxAutoDetectCookieSupport%3d1")

            try:
                self.driver.find_element('xpath',"//input[@value='Accept']").click()
            except:
                pass
            
            sleep(3)

            try:
                self.driver.find_element('xpath',"(//input[@value='Search'])[3]").click()
            except:
                try:
                    self.driver.find_element('xpath',"(//input[@value='Search'])[3]").click()
                except:
                    pass
            sleep(5)

            page = self.driver.page_source
            html = Selector(text=page)

            links = html.xpath("//h2/a/@href").getall()
            for i in links:
                abs_i  =f'https://planning.dorsetcouncil.gov.uk/{i}'
                self.listhref.append(abs_i)

            x = 1
            while True:
                try:
                    nextPl = self.driver.find_element('xpath',"(//a[text()='Next'])[1]")
                    self.driver.execute_script("arguments[0].scrollIntoView();", nextPl)
                    self.driver.execute_script("arguments[0].click();", nextPl)
                    sleep(3)
                    x += 1
                    print(f'{x} page scraped')
                    print(f'{x} page scraped')
                    print(f'{x} page scraped')
                    print(f'{x} page scraped')
                    page = self.driver.page_source
                    html = Selector(text=page)

                    page = self.driver.page_source
                    html = Selector(text=page)

                    links = html.xpath("//h2/a/@href").getall()
                    for i in links:
                        abs_i  =f'https://planning.dorsetcouncil.gov.uk/{i}'
                        self.listhref.append(abs_i)
                    break

                except:
                    break

