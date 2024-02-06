import scrapy
from planners.util import dates_strx
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.common.by import By

import ddddocr


options = FirefoxOptions()
# options.add_argument("--headless")
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


class NuneatonandbedworthSpider(scrapy.Spider):
    name = "nuneatonandbedworth"
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
        # dispatcher.connect(self.spider_closed,signals.spider_closed)

    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
            self.driver.get("https://customer.nuneatonandbedworth.gov.uk/en/AchieveForms/?form_uri=sandbox-publish://AF-Process-bb4f1551-25f7-4c9d-9504-359555b4764c/AF-Stage-52bb890a-7580-4889-8b19-31d27fd8a3bd/definition.json&redirectlink=/en&cancelRedirectLink=/en&consentMessage=yes&noLoginPrompt=1")
            sleep(10)
            
            try:
                self.driver.find_element('xpath',"//button[contains(@id,'close-cookie-message')]").click()
            except:
                pass
            sleep(5)
            try:
                self.driver.find_element('xpath',"(//span[@class='radio-wrapper'])[1]").click()
            except:
                pass
            
            sleep(3)
            print(self.driver.page_source)
            
            # for i in list(range(0,1)):
            #     i = str(i)
            #     if len(i) == 1:
            #         i = f'00000{i}'
            #     elif len(i) == 2:
            #         i = f'0000{i}'
            #     elif len(i) == 3:
            #         i = f'000{i}'
            #     elif len(i) == 4:
            #         i = f'00{i}'
            #     elif len(i) == 5:
            #         i = f'0{i}'
            #     try:
            #         #date picker
            #         fromDate = self.driver.find_element("xpath","//input[@id='applicationReferenc']")

            #         fromDate.clear()

            #         fromDate.send_keys("040062")
            #         self.driver.find_element("xpath","//button[@id='PLsearch']").click()
            #         sleep(2)

                    
                    
                            
            #     except:
            #         continue

            
                
                
            #     captcha = self.driver.find_element("xpath", "//textarea[@id='concatDetails']")
            #     captcha.screenshot(f'captcha.png')

            #     ocr = ddddocr.DdddOcr()
            #     # open and read the image
            #     with open(f'captcha.png', 'rb') as f:
            #         img_bytes = f.read()

            #     res = ocr.classification(img_bytes)
            #     print(res.upper())
