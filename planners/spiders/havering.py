import scrapy
from planners.util import dates_str2
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


class HaveringSpider(scrapy.Spider):
    name = "havering"
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
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    
    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
            for opt in list(range(1,22)):
                start = 0
                for d in dates_str2[0:-1]:
                    start += 1
                    fd = d
                    nd = dates_str2[start]

                    self.driver.get("https://development.havering.gov.uk/OcellaWeb/planningSearch")
                    try:
                        self.driver.find_element('xpath',"//select[@id='area']").click()
                    except:
                        try:
                            self.driver.find_element('xpath',"//select[@id='area']").click()
                        except:
                            pass
                    
                    try:
                        all = self.driver.find_elements('xpath',"//select[@id='area']/option")
                        all[opt].click()
                    except:
                        try:
                            all = self.driver.find_elements('xpath',"//select[@id='area']/option")
                            all[opt].click()
                        except:
                            pass
                    
                    #date picker
                    fromDate = self.driver.find_element("xpath","//input[@id='receivedFrom']")

                    fromDate.clear()

                    fromDate.send_keys(fd)

                    fromto = self.driver.find_element("xpath","//input[@id='receivedTo']")
                    fromto.clear()

                    fromto.send_keys(nd)

                    try:
                        self.driver.find_element('xpath',"//input[@value='Search']").click()
                    except:
                        try:
                            self.driver.find_element('xpath',"//input[@value='Search']").click()
                        except:
                            pass
                    
                    try:
                        self.driver.find_element('xpath',"//input[@value='Show all results']").click()
                    except:
                        pass

                    pagex = self.driver.page_source
                    html = Selector(text=pagex)
                    links = html.xpath("//table/descendant::a/@href").getall()
                    self.listhref.extend(links)
                    print('Date search')
                    print(f'From {fd} to {nd}')
                    print(f'From {fd} to {nd}')
                    print(f'From {fd} to {nd}')
                    

            
            for i in self.listhref:
                abs_i = f'https://development.havering.gov.uk/OcellaWeb/{i}'
                self.drivera.get(abs_i)

                
                pagey = self.drivera.page_source
                htmla = Selector(text=pagey)
                    
                
                each = {}

                
                table_hd = htmla.xpath("//table[2]/descendant::tr/td[1]")
                for i in table_hd:
                    first = i.xpath(".//descendant::text()").get()
                    second = i.xpath(".//following-sibling::td/descendant::text()").getall()
                    if second:
                        second = ''.join(second)
                        second = stripper(second)

                    try:
                        fir = camel_case(first)

                        each[fir] = second
                    except:
                        each[first] = second
                if each:
                    yield each
                    self.total.append(each)
                    


                            
    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()
        spider.logger.info("Spider closed: %s", spider.name)
    