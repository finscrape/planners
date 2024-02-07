import scrapy
from planners.util import dates_str3
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


class StaffsmoorlandsSpider(scrapy.Spider):
    name = "staffsmoorlands"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()


        self.drivera = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
        self.drivera.maximize_window()
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    
    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
    
        self.driver.get("http://publicaccess.staffsmoorlands.gov.uk/portal/servlets/ApplicationSearchServlet")
        
        #date picker
        sleep(60)
        try:
            self.driver.find_element('xpath',"//input[@value='Search']").click()
        except:
            try:
                self.driver.find_element('xpath',"//input[@value='Search']").click()
            except:
                pass
        
        pagex = self.driver.page_source
        html = Selector(text=pagex)
        links = html.xpath("//td/a/@href").getall()
        self.listhref.extend(links)
        print('Date search')
        print('From 1900 to 2024')
        print('From 1900 to 2024')
        print('From 1900 to 2024')
        x = 0
        while True:
            x+=1
            try:
                self.driver.find_element("xpath","//input[@value='Next Matching Results']").click()
                
                page = self.driver.page_source
                html = Selector(text=page)
                links = html.xpath("//td/a/@href").getall()
                print(f'Next Date search..page{x}')
                print('From 1900 to 2024')
                print('From 1900 to 2024')
                print('From 1900 to 2024')
                
                self.listhref.extend(links)
                
            except:
                break

        print(self.listhref)
        for i in self.listhref:
            i = i.replace("..","")
            abs_i  =f'http://publicaccess.staffsmoorlands.gov.uk/portal{i}'
            self.drivera.get(abs_i)
            sleep(1)

            pagex = self.drivera.page_source
            htmla = Selector(text=page)

            each = {}
            url = response.url
            each['url'] = url
            

            cons_doc = []
            rd = htmla.xpath("//th[text()='Consultations']/ancestor::tr/following-sibling::tr")
            if rd:
                for i in rd[1:]:
                    e_rel={}
                    e_rel['name'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                    e_rel['address'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                    cons_doc.append(e_rel)
            
            
            
            table_hd = htmla.xpath("//form[@name='formPLNDetails']/table/descendant::tr/td/b")
            if table_hd:
                for i in table_hd:
                    first = i.xpath(".//descendant::text()").get()
                    second = i.xpath(".//ancestor::td[1]/following-sibling::td[1]/descendant::text()").getall()
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

            each['allConsulteeDetails'] = cons_doc
            yield each
            self.total.append(each)
            
    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()
        spider.logger.info("Spider closed: %s", spider.name)
                        

                
                        
                        
                        


