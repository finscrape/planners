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

class TamworthSpider(scrapy.Spider):
    name = "tamworth"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = 0
        self.total = []
        self.driver = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
        self.driver.maximize_window()

        dispatcher.connect(self.spider_closed,signals.spider_closed)

    
    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")


    def start_requests(self):
        yield scrapy.Request(url="https://planning.tamworth.gov.uk/northgate/planningexplorer/generalsearch.aspx")
    def parse(self, response):
        link = response.xpath("//select[@name='cboWardCode']/option/text()").getall()
        x = 1
        for i in link[1:]:

        
            self.driver.get("https://planning.tamworth.gov.uk/northgate/planningexplorer/generalsearch.aspx")

            self.driver.find_element("xpath","//select[@name='cboWardCode']").click()
            opt = self.driver.find_elements("xpath","//select[@name='cboWardCode']/option")
            opt[x].click()
            x += 1
            

            self.driver.find_element('xpath',"//input[@name='csbtnSearch']").click()


            page = self.driver.page_source
            html = Selector(text=page)
            links = html.xpath("//td[@class='TableData']/a/@href").getall()
            self.listhref.extend(links)
            

            last = html.xpath("//span[@id='lblPagePosition']/text()").get()
            l = last.split('of')
            lastt = int(l[-1])


            start = 1
            while start < lastt:
                try:
                    self.driver.find_element("xpath","//img[@alt='Go to next page ']").click()
                    page = self.driver.page_source
                    html = Selector(text=page)
                    links = html.xpath("//td[@class='TableData']/a/@href").getall()
                    self.listhref.extend(links)
                    
                except:
                    break


                start +=1
            
    
        for o in self.listhref:
            abs_i = f'https://planning.tamworth.gov.uk/Northgate/PlanningExplorerAA/Generic/{o}'
            yield scrapy.Request(url=abs_i,callback=self.each)


    def each(self,response):
        each = {}
        row = response.xpath("//div[@class='content node-landing-page']/descendant::span")
        for i in row:
            head = i.xpath(".//text()").get()
            body = i.xpath(".//following-sibling::text()").getall()
            bodyall = ''.join(body)
            bodyall = bodyall.replace('\r','').replace('\n','').replace('\t','').strip()

            fir = camel_case(head)

            each[fir] = bodyall
        yield each
        self.total.append(each)
        

    def spider_closed(self, spider):
        self.driver.close()
        spider.logger.info("Spider closed: %s", spider.name)
        
            