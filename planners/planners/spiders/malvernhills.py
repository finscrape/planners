import scrapy
from planners.util import dates_str
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


class MalvernhillsSpider(scrapy.Spider):
    name = "malvernhills"
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
            self.driver.get("https://plan.malvernhills.gov.uk/Search/Advanced")

            try:
                self.driver.find_element('xpath',"//input[@value='Agree']").click()
            except:
                pass

            try:
                self.driver.find_element('xpath',"//input[@id='SearchPlanning']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//input[@id='SearchPlanning']").click()
                except:
                    print('error with plannin mutton')
            

            try:
                self.driver.find_element('xpath',"//button[@id='submitBtn']").click()
                
            except:
                sleep(60)
                self.driver.find_element('xpath',"//button[@id='submitBtn']").click()
            

            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//table[@class='table-striped tblResults']/descendant::a/@href").getall()
            self.listhref.extend(links)
            
            x = 0
            while True:
                x += 1
                if x > 7139:
                    break
                try:
                    self.driver.find_element("xpath","//a[@aria-label='Next Page.']").click()
                    page = self.driver.page_source
                    html = Selector(text=page)
                    links = html.xpath("//table[@class='table-striped tblResults']/descendant::a/@href").getall()
                    self.listhref.extend(links)
                    
                except:
                    pass
            
            
            for i in self.listhref:
                abs_i = f'https://plan.malvernhills.gov.uk{i}'
                yield scrapy.Request(url=abs_i,meta={'u':abs_i},callback=self.parsedetails,dont_filter=True)

    def parsedetails(self,response):
        
        box0 = response.xpath("//div[@id='MainDetails']/descendant::tr/td[1]")
        
        each = {}
        each['planningUrl'] = response.url
        nei_doc = []
        rd = response.xpath("(//table[@class='tblTest table'])[1]/descendant::tr")
        for i in rd[1:]:
            e_rel={}
            e_rel['name'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
            e_rel['address'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            e_rel['sent'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
            e_rel['replyReceived'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
            nei_doc.append(e_rel)


        cons_doc = []
        rd = response.xpath("(//table[@class='tblTest table'])[2]/descendant::tr")
        for i in rd[1:]:
            e_rel={}
            e_rel['name'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
            e_rel['organisation'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
            e_rel['sent'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
            e_rel['replyDue'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
            
            e_rel['replyReceived'] = stripper(i.xpath(".//td[5]/descendant::text()").get())
            cons_doc.append(e_rel)

        sum_doc = []
        rd = response.xpath("(//table[@class='summaryTbl table'])[4]/descendant::tr/td/descendant::text()").getall()
        rd_r = rd[1:]
        sum_doc.extend(rd_r)


        for i in box0[1:]:
            first = i.xpath(".//text()").get()
            if first and first != 'summary':
                second = i.xpath(".//following-sibling::td/descendant::text()").getall()
                second = ''.join(second)
                
                second = stripper(second)

                try:
                    fir = camel_case(first)

                    each[fir] = second
                except:
                    each[first] = second

        
        each['neighbourList'] = nei_doc
        each['consulteeList'] = cons_doc
        each['constraintsList'] = sum_doc

        yield each
        self.total.append(each)
    
    def spider_closed(self, spider):
        self.driver.close()
        
        spider.logger.info("Spider closed: %s", spider.name)
    