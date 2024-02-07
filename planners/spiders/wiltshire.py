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


class WiltshireSpider(scrapy.Spider):
    name = "wiltshire"
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
        for opt in list(range(1,102)):
            self.driver.get("https://development.wiltshire.gov.uk/pr/s/?tabset-167f1=3")
            sleep(1.5)
            try:
                self.driver.find_element('xpath',"//label[contains(text(),'Ward')]/following-sibling::div/select").click()
            except:
                try:
                    self.driver.find_element('xpath',"//label[contains(text(),'Ward')]/following-sibling::div/select").click()
                except:
                    pass
            sleep(1)
            try:
                all = self.driver.find_elements('xpath',"//label[contains(text(),'Ward')]/following-sibling::div/select/option")
                all[opt].click()
            except:
                try:
                    all = self.driver.find_elements('xpath',"//label[contains(text(),'Ward')]/following-sibling::div/select/option")
                    all[opt].click()
                except:
                    pass

            try:
                self.driver.find_element('xpath',"(//button[@name='submit'])[2]").click()
            except:
                try:
                    self.driver.find_element('xpath',"(//button[@name='submit'])[2]").click()
                except:
                    pass
            sleep(10)

            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//a[@dir='ltr']/@href").getall()
            self.listhref.extend(links)

            x = 0
            while True:
                try:
                    self.driver.find_element("xpath","//button[text()='Next']").click()
                    sleep(0.3)
                    
                    page = self.driver.page_source
                    html = Selector(text=page)
                    check = html.xpath("//button[text()='Next']/@disabled").get()
                    if check:
                        break
                    links = html.xpath("//a[@dir='ltr']/@href").getall()
                    print(f'Next page {x}')
                    print(f'Next page {x}')
                    print(f'Next page {x}')
                    self.listhref.extend(links)
                    
                except:
                    break



        for i in self.listhref:
                abs_i = f'https://development.wiltshire.gov.uk{i}'
                self.drivera.get(abs_i)
                crl = self.drivera.current_url
                
                
                sleep(2.5)

                each = {}
                each['url'] =crl
                
                htmlcase = self.drivera.page_source
                page = Selector(text=htmlcase)
                

                
                each['siteAddress'] = page.xpath("//span[text()='Site Address']/ancestor::div[1]/descendant::text()[2]").get()
                each['proposal'] = page.xpath("//span[text()='Proposal']/ancestor::div[1]/descendant::text()[2]").get()
                table_hd = page.xpath("//span[@class='test-id__field-label']")
                if table_hd:
                    for i in table_hd:
                        first = i.xpath(".//descendant::text()").get()
                        if first:
                            second = i.xpath(".//ancestor::div[1]/following-sibling::div[1]/descendant::text()").getall()
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
                        

                
                        
                        
                        



            
    