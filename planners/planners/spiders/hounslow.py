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


class HounslowSpider(scrapy.Spider):
    name = "hounslow"
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
            for opt in list(range(1,7)):
            
                self.driver.get("https://planning.hounslow.gov.uk/Planning_Search_Advanced.aspx")

                try:
                    self.driver.find_element('xpath',"//input[@value='Accept the Terms and Conditions']").click()
                except:
                    try:
                        self.driver.find_element('xpath',"//input[@value='Accept the Terms and Conditions']").click()
                    except:
                        pass
                
                sleep(5)
                try:
                    self.driver.find_element('xpath',"//a[@href='planning_search.aspx']").click()
                except:
                    try:
                        self.driver.find_element('xpath',"//a[@href='planning_search.aspx']").click()
                    except:
                        pass
                sleep(5)
                try:
                    self.driver.find_element('xpath',"//li[a/@href='Planning_Search_Advanced.aspx']").click()
                except:
                    try:
                        self.driver.find_element('xpath',"//li[a/@href='Planning_Search_Advanced.aspx']").click()
                    except:
                        pass
                sleep(5)
                try:
                    self.driver.find_element('xpath',"//select[@id='MainContent_ddArea']").click()
                except:
                    try:
                        self.driver.find_element('xpath',"//select[@id='MainContent_ddArea']").click()
                    except:
                        pass
                sleep(5)
                try:
                    all = self.driver.find_elements('xpath',"//select[@id='MainContent_ddArea']/option")
                    all[opt].click()
                except:
                    try:
                        all = self.driver.find_elements('xpath',"//select[@id='MainContent_ddArea']/option")
                        all[opt].click()
                    except:
                        pass
                
                try:
                    self.driver.find_element('xpath',"//input[@id='MainContent_btn_Search']").click()
                except:
                    try:
                        self.driver.find_element('xpath',"//input[@id='MainContent_btn_Search']").click()
                    except:
                        pass
                sleep(3)

                pagex = self.driver.page_source
                html = Selector(text=pagex)
                links = html.xpath("//strong/a/@href").getall()
                self.listhref.extend(links)

                last = html.xpath("//span[@id='MainContent_PageCountLabel']/text()").get()
                intlast = int(last)

                x = 0
                while True:
                    x += 1
                    if x > intlast:
                        break
                    try:
                        self.driver.find_element("xpath","//a[@id='MainContent_NextLink']").click()
                        sleep(1)
                        page = self.driver.page_source
                        html = Selector(text=page)
                        links = html.xpath("//strong/a/@href").getall()
                        self.listhref.extend(links)

                        check = html.xpath("//span[@id= 'MainContent_lbl_Text']/text()").getall()
                        allc = ''.join(check)

                        print(allc)
                        print(allc)
                        print(allc)
                        print(f'Which committee?---{x} pages')
                        
                    except:
                        pass
                
                
                for i in self.listhref:
                    abs_i = f'https://planning.hounslow.gov.uk/{i}'
                    self.drivera.get(abs_i)
                    
                    try:
                        self.drivera.find_element('xpath',"//input[@value='Accept the Terms and Conditions']").click()
                    except:
                        try:
                            self.drivera.find_element('xpath',"//input[@value='Accept the Terms and Conditions']").click()
                        except:
                            pass
                    
                    sleep(1)
                    try:
                        self.drivera.find_element('xpath',"//a[@href='planning_search.aspx']").click()
                    except:
                        try:
                            self.drivera.find_element('xpath',"//a[@href='planning_search.aspx']").click()
                        except:
                            pass
                    sleep(1)

                    abs_spl = abs_i.split("=")
                    caseNo = abs_spl[-1]

                    try:
                        caseinput = self.drivera.find_element('xpath',"//input[@id='MainContent_txt_App_No']")
                        caseinput.clear()

                        caseinput.send_keys(caseNo)

                    except:
                        try:
                            caseinput = self.drivera.find_element('xpath',"//input[@id='MainContent_txt_App_No']")
                            caseinput.clear()

                            caseinput.send_keys(caseNo)

                        except:
                            pass
                    


                    try:
                        self.drivera.find_element('xpath',"//input[@id='MainContent_btn_QuickSearch']").click()
                    except:
                        try:
                            self.drivera.find_element('xpath',"//input[@id='MainContent_btn_QuickSearch']").click()
                        except:
                            pass
                    
                    
                    each = {}

                    htmlcase = self.drivera.page_source
                    page = Selector(text=htmlcase)
                    

                    desc = page.xpath("//h2/descendant::text()").get()
                    each['titleDescription'] = desc

                    prop = page.xpath("//span[@id='MainContent_lbl_Proposal']/descendant::text()").get()
                    each['proposal'] = prop
                    
                    
                    table_hd = page.xpath("//dt")
                    for i in table_hd:
                        first = i.xpath(".//descendant::text()").get()
                        second = i.xpath(".//following-sibling::dd/descendant::text()").getall()
                        if second:
                            second = ''.join(second)
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
    
                    
                            
                            
                            