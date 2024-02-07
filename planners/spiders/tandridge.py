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

class TandridgeSpider(scrapy.Spider):
    name = "tandridge"
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
            for opt in list(range(2,25)):
                self.driver.get("https://tdcplanningsearch.tandridge.gov.uk/Default#TDCInfo")

                try:
                    self.driver.find_element('xpath',"//select[@id='MainContent_ddlSearchCriteria']").click()
                except:
                    try:
                        self.driver.find_element('xpath',"//select[@id='MainContent_ddlSearchCriteria']").click()
                    except:
                        pass
                sleep(3)
                try:
                    all = self.driver.find_elements('xpath',"//select[@id='MainContent_ddlSearchCriteria']/option")
                    all[2].click()
                except:
                    try:
                        all = self.driver.find_elements('xpath',"//select[@id='MainContent_ddlSearchCriteria']/option")
                        all[2].click()
                    except:
                        pass
                sleep(3)


                try:
                    self.driver.find_element('xpath',"//select[@id='MainContent_ddlParish']").click()
                except:
                    try:
                        self.driver.find_element('xpath',"//select[@id='MainContent_ddlParish']").click()
                    except:
                        pass
                sleep(1)
                try:
                    all = self.driver.find_elements('xpath',"//select[@id='MainContent_ddlParish']/option")
                    all[opt].click()
                except:
                    try:
                        all = self.driver.find_elements('xpath',"//select[@id='MainContent_ddlParish']/option")
                        all[opt].click()
                    except:
                        pass

                
                try:
                    caseinput = self.driver.find_element('xpath',"//input[@id='MainContent_txtStartDate']")
                    caseinput.clear()

                    caseinput.send_keys('01/01/1900')

                except:
                    pass
                try:
                    caseoutput = self.driver.find_element('xpath',"//input[@id='MainContent_txtEndDate']")
                    caseoutput.clear()

                    caseoutput.send_keys('01/01/2024')

                except:
                    pass

        
        
                
                
                try:
                    self.driver.find_element('xpath',"//input[@id='MainContent_btnSearch']").click()
                except:
                    try:
                        self.driver.find_element('xpath',"//input[@id='MainContent_btnSearch']").click()
                    except:
                        pass
                sleep(30)


                try:
                    self.driver.find_element('xpath',"//select[@name='tblSearchResult_length']").click()
                except:
                    try:
                        self.driver.find_element('xpath',"//select[@name='tblSearchResult_length']").click()
                    except:
                        pass
                sleep(1)
                try:
                    all = self.driver.find_elements('xpath',"//select[@id='tblSearchResult_length']/option")
                    all[3].click()
                except:
                    try:
                        all = self.driver.find_elements('xpath',"//select[@id='tblSearchResult_length']/option")
                        all[3].click()
                    except:
                        pass

                pagex = self.driver.page_source
                html = Selector(text=pagex)
                links = html.xpath("//tr[contains(@class,'DataRow')]/td[1]/a/text()").getall()
                self.listhref.extend(links)

                x = 0
                while True:
                    x += 1
                    try:
                        self.driver.find_element("xpath","//a[@class='paginate_button next']").click()
                        sleep(1)
                        
                        page = self.driver.page_source
                        html = Selector(text=page)
                        links = html.xpath("//tr[contains(@class,'DataRow')]/td[1]/a/text()").getall()
                        note = html.xpath("//div[@id='dvRecsFound']/descendant::p/text()[1]").get()
                        number = html.xpath("//div[@id='tblSearchResult_info']/text()").get()
                        print(note)
                        print(number)
                        print(number)
                        self.listhref.extend(links)
                        
                    except:
                        break

            for i in self.listhref:

                self.drivera.get("https://tdcplanningsearch.tandridge.gov.uk/Default#TDCInfo")

                try:
                    self.drivera.find_element('xpath',"//select[@id='MainContent_ddlSearchCriteria']").click()
                except:
                    try:
                        self.drivera.find_element('xpath',"//select[@id='MainContent_ddlSearchCriteria']").click()
                    except:
                        pass
                sleep(2)
                try:
                    all = self.drivera.find_elements('xpath',"//select[@id='MainContent_ddlSearchCriteria']/option")
                    all[1].click()
                except:
                    try:
                        all = self.drivera.find_elements('xpath',"//select[@id='MainContent_ddlSearchCriteria']/option")
                        all[1].click()
                    except:
                        pass
                
                try:
                    ref_input = self.drivera.find_element('xpath',"//input[@id='MainContent_txtPlanningAppRef']")
                    ref_input.clear()

                    ref_input.send_keys(i)

                except:
                    pass

                try:
                    self.drivera.find_element('xpath',"//input[@id='MainContent_btnSearch']").click()
                except:
                    try:
                        self.drivera.find_element('xpath',"//input[@id='MainContent_btnSearch']").click()
                    except:
                        pass
                sleep(2)

                try:
                    self.drivera.find_element('xpath',"//tr[contains(@class,'DataRow')]/td[1]/a").click()
                except:
                    try:
                        self.drivera.find_element('xpath',"//tr[contains(@class,'DataRow')]/td[1]/a").click()
                    except:
                        pass

                
                sleep(2)

                each = {}

                htmlcase = self.drivera.page_source
                page = Selector(text=htmlcase)
                

                rel_doc = []
                rd = page.xpath("//table[@id='tblConsultee']/descendant::tr")
                if rd:
                    for i in rd[1:]:
                        e_rel={}
                        e_rel['consulteeDetails'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                        e_rel['address'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                        e_rel['type'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                        e_rel['correspondenceDate'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                        rel_doc.append(e_rel)
                
                con_doc = []
                rd = page.xpath("//table[@aria-describedby='tblConstraints_info']/descendant::tr")
                if rd:
                    for i in rd[1:]:
                        e_rel={}
                        e_rel['subCode'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                        e_rel['description'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                        con_doc.append(e_rel)

                
                table_hd = page.xpath("//span[@class='control-label']")
                if table_hd:
                    for i in table_hd:
                        first = i.xpath(".//descendant::text()").get()
                        second = i.xpath(".//ancestor::div[1]/following-sibling::div[1]/descendant::span[@class='DataValue']/text()").getall()
                        if second:
                            second = ''.join(second)
                            second = stripper(second)

                        try:
                            fir = camel_case(first)

                            each[fir] = second
                        except:
                            each[first] = second
                if each:
                    each['allConsulteeDetails'] = rel_doc
                    each['allConstraintsDetails'] = con_doc
                    yield each
                    self.total.append(each)
                    
    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()
        spider.logger.info("Spider closed: %s", spider.name)
                        

                
                        
                        
                        

