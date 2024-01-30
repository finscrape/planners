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


class SaltfordcitySpider(scrapy.Spider):
    name = "saltfordcity"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = 0
        self.total = []
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
        self.driver.maximize_window()

        self.drivera = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
        self.drivera.maximize_window()


        dispatcher.connect(self.spider_closed,signals.spider_closed)

    
    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
        start=0
        for d in dates_str[0:-1]:
                    
            start += 1
            fd = d
            nd = dates_str[start]

            self.driver.get('https://salfordcitycouncil.my.site.com/pr/s/register-view?c__r=Arcus_BE_Public_Register')
            sleep(3)
            try:
                self.driver.find_element('xpath',"//button[text()='Advanced search']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//button[text()='Advanced search']").click()
                except:
                    pass


            
            

            sleep(3)
            #date picker
            fromDate = self.driver.find_element("xpath","//label[text()='Valid date from']/following-sibling::div/input")

            fromDate.clear()

            fromDate.send_keys(fd)

            fromto = self.driver.find_element("xpath","//label[text()='Valid date to']/following-sibling::div/input")
            fromto.clear()

            fromto.send_keys(nd)

            try:
                self.driver.find_element('xpath',"//button[text()='Search']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//button[text()='Search']").click()
                except:
                    pass
            
            sleep(3)

            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//lightning-formatted-url/a/@href").getall()
            self.listhref.extend(links)

            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
            
            x = 0
            while True:
                x += 1
                try:
                    searchPl = self.driver.find_element("xpath","//a[contains(text(),'Next')]")
                    self.driver.execute_script("arguments[0].scrollIntoView();", searchPl)
                    self.driver.execute_script("arguments[0].click();", searchPl)
                    
                    sleep(2)
                    page = self.driver.page_source
                    html = Selector(text=page)
                    links = html.xpath("//lightning-formatted-url/a/@href").getall()
                    self.listhref.extend(links)
                    print(f'From {fd} to {nd}------getting the {x} pageeee')
                    print(f'From {fd} to {nd}------getting the {x} pageeee')
                    print(f'From {fd} to {nd}------getting the {x} pageeee')

                    
                except:
                    break

            
        for i in self.listhref:
            abs_i = f'https://salfordcitycouncil.my.site.com{i}'
            self.drivera.get(abs_i)
            sleep(2)

            pagex = self.drivera.page_source
            htmla = Selector(text=pagex)
            
            each = {}
            each['planningUrl'] = self.drivera.current_url
            each['planningApplication'] = htmla.xpath("//h1/text()").get()

            table_hd = htmla.xpath("//dt[@class='pr-summary-list__key']")
            for i in table_hd:

                first = i.xpath(".//descendant::text()").get()
                if first and first != "  ":
                    second = i.xpath(".//following-sibling::dd[1]/descendant::text()").getall()
                    if second:
                        second = ''.join(second)
                        second = stripper(second)
                    else:
                        second = ""
                    try:
                        fir = camel_case(first)

                        each[fir] = second
                    except:
                        each[first] = second

            
            if each:
                self.plan +=1
                print(f'{self.plan} planning application')
                print(f'{self.plan} planning application')
                print(f'{self.plan} planning application')
                print(f'{self.plan} planning application')
                yield each
                self.total.append(each)
                
    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()
        spider.logger.info("Spider closed: %s", spider.name)
                        
