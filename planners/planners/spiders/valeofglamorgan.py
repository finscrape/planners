import scrapy
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

class ValeofglamorganSpider(scrapy.Spider):
    name = "valeofglamorgan"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
        self.driver.maximize_window()

        # self.drivera = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
        # self.drivera.maximize_window()


        #dispatcher.connect(self.spider_closed,signals.spider_closed)

    
    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
            self.driver.get("https://vogonline.planning-register.co.uk/Search/Planning/Advanced")
            try:
                self.driver.find_element('xpath',"//button[text()='Close']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//button[text()='Close']").click()
                except:
                    pass
            
            try:
                self.driver.find_element('xpath',"//input[@id='submitSearchButton']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//input[@id='submitSearchButton']").click()
                except:
                    pass
            sleep(3)

            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//table[@class='table searchResultsTable']/descendant::tr/descendant::a[contains(@href,'Planning')]/@href").getall()
            self.listhref.extend(links)
            print(self.listhref) 

            x = 0
            while True:
                x += 1
                try:
                    self.driver.find_element("xpath","//a[@aria-label='Next Page.']").click()
                    page = self.driver.page_source
                    html = Selector(text=page)
                    links = html.xpath("//table[@class='table searchResultsTable']/descendant::tr/descendant::a[contains(@href,'Planning')]/@href").getall()
                    self.listhref.extend(links)
                    print(f'Next Page ----{x} ')
                    print(f'Next Page ----{x} ')
                    print(f'Next Page ----{x} ')
                    sleep(3)
                    
                except:
                    break

            for i in self.listhref:
                abs_i = f'https://vogonline.planning-register.co.uk{i}'
                yield scrapy.Request(url=abs_i,meta={'u':abs_i},callback=self.parsedetails,dont_filter=True)

    def parsedetails(self,response):
        
        
        each = {}
        pub_doc = []
        rd = response.xpath("(//table[@class='publicNoticesTable'])[1]/descendant::tr")
        for i in rd[1:]:
            e_rel={}
            e_rel['number'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
            e_rel['siteOrPress'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            e_rel['description'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
            e_rel['displayDate'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
            pub_doc.append(e_rel)


        cons_doc = []
        rd = response.xpath("(//table[@class='consulteesTable table-striped'])/descendant::tr")
        for i in rd[1:]:
            e_rel={}
            e_rel['name'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
            e_rel['dateSent'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            e_rel['type'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
            e_rel['expiryDate'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
            
            cons_doc.append(e_rel)

        code_doc = []
        rd = response.xpath("(//table[@class='conditionsTable table-striped'])/descendant::tr")
        for i in rd[1:]:
            e_rel={}
            e_rel['code'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
            e_rel['conditionDetails'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            
            code_doc.append(e_rel)

        nei_doc = []
        rd = response.xpath("(//table[@class='neighboursTable table-striped'])[1]/descendant::tr")
        for i in rd[1:]:
            e_rel={}
            e_rel['address'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
            e_rel['dateSent'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            e_rel['reconsultDate'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
            e_rel['expiryDate'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
            nei_doc.append(e_rel)


        ctr_doc = []
        rd = response.xpath("(//table[@class='constraintsTable'])[1]/descendant::tr")
        for i in rd[1:]:
            e_rel={}
            e_rel['number'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
            e_rel['description'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            ctr_doc.append(e_rel)

        doc_doc = []
        rd = response.xpath("(//table[@class='table sortable document-list'])[1]/descendant::tr[@class='row_link']")
        for i in rd[1:]:
            e_rel={}
            e_rel['name'] = stripper(i.xpath(".//td[2]/descendant::a/text()").get())
            e_rel['link'] = "https://vogonline.planning-register.co.uk" + stripper(i.xpath(".//td[2]/descendant::a/@href").get())
            e_rel['date'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
            doc_doc.append(e_rel)

        
        box0 = response.xpath("//dt")
        
        for i in box0:
            first = i.xpath(".//descendant::text()").get()
            if first and first != 'summary':
                second = i.xpath(".//following-sibling::dd[1]/descendant::text()").getall()
                second = ''.join(second)
                
                second = stripper(second)

                try:
                    fir = camel_case(first)

                    each[fir] = second
                except:
                    each[first] = second

        
        each['neighbour'] = nei_doc
        each['consultees'] = cons_doc
        each['constraints'] = ctr_doc
        each['publicNotices'] = pub_doc
        each['documents'] = doc_doc
        each['code'] = code_doc

        yield each
        self.total.append(each)
    
    def spider_closed(self, spider):
        self.driver.close()
        
        spider.logger.info("Spider closed: %s", spider.name)
               
            
            