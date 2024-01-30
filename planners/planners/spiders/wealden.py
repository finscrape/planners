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


class WealdenSpider(scrapy.Spider):
    name = "wealden"
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
            self.driver.get("https://planning.wealden.gov.uk/disclaimer.aspx")

            try:
                self.driver.find_element('xpath',"//input[@id='ctl00_ContentPlaceHolder1_btnAccept']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//input[@id='ctl00_ContentPlaceHolder1_btnAccept']").click()
                except:
                    pass

            sleep(3)

            try:
                self.driver.find_element('xpath',"(//a[contains(text(),'Advanced Search')])[2]").click()
            except:
                pass
            
            sleep(2)
            pagea = self.driver.page_source
            htmla = Selector(text=pagea)
            check = htmla.xpath("//input[@id='ctl00_ContentPlaceHolder1_chklstSearchType_0']/@checked").get()
            if check != 'checked':
                try:
                    self.driver.find_element('xpath',"//input[@id='ctl00_ContentPlaceHolder1_chklstSearchType_0']").click()
                except:
                    try:
                        self.driver.find_element('xpath',"//input[@id='ctl00_ContentPlaceHolder1_chklstSearchType_0']").click()
                    except:
                        print('error with plannin mutton')
                sleep(3)
            
            try:
                self.driver.find_element('xpath',"//input[@name='ctl00$ContentPlaceHolder1$btnSearch']").click()
                
            except:
                
                pass

            sleep(5)
            sleep(1)
            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//h2/a/@href").getall()
            self.listhref.extend(links)
            x = 0
            while True:
                x += 1
                if x > 13956:
                    break
                try:
                    self.driver.find_element("xpath","(//input[@class='rdpPageNext'])[1]").click()
                    sleep(2)
                    page = self.driver.page_source
                    html = Selector(text=page)
                    links = html.xpath("//h2/a/@href").getall()
                    last = html.xpath("(//div[@class='rdpWrap'])[6]/text()").get()
                    print('Advanced search')
                    print(last)
                    print(last)
                    print(last)
                    self.listhref.extend(links)
                    
                except:
                    break
            
            for i in self.listhref:
                abs_i = f'https://planning.wealden.gov.uk/{i}'
                self.drivera.get(abs_i)

                try:
                    self.drivera.find_element('xpath',"//input[@id='ctl00_ContentPlaceHolder1_btnAccept']").click()
                    sleep(2)
                except:
                    try:
                        self.drivera.find_element('xpath',"//input[@id='ctl00_ContentPlaceHolder1_btnAccept']").click()
                        sleep(2)
                    except:
                        pass
                    
                
                pagey = self.drivera.page_source
                htmla = Selector(text=pagey)
                    
                
                each = {}

                nei_doc = []
                rd = htmla.xpath("(//table[@id='ctl00_ContentPlaceHolder1_gridConsultees'])[1]/descendant::tr")
                for i in rd[1:]:
                    e_rel={}
                    e_rel['name'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                    e_rel['sent'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                    e_rel['replyDue'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                    e_rel['replyReceived'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                    nei_doc.append(e_rel)

                table_hd = htmla.xpath("//span[@class='applabel']")
                for i in table_hd:
                    first = i.xpath(".//descendant::text()").get()
                    first=stripper(first)
                    second = i.xpath(".//following-sibling::p/descendant::text()").getall()
                    if second:
                        second = ''.join(second)
                        second = stripper(second)

                    try:
                        fir = camel_case(first)

                        each[fir] = second
                    except:
                        each[first] = second
                if each:
                    each['consultees'] = nei_doc
                    each['appeals'] = stripper(htmla.xpath("//div[@id='ctl00_ContentPlaceHolder1_panNoAppeals']/descendant::text()").get())
            
                    yield each
                    self.total.append(each)
                    


    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()
        spider.logger.info("Spider closed: %s", spider.name)
                        
