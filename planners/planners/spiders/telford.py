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

class TelfordSpider(scrapy.Spider):
    name = "telford"
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

    def parse(self, response):
        self.driver.get("https://secure.telford.gov.uk/planningsearch/")

        try:
            self.driver.find_element("xpath","//input[@type='submit']").click()
            sleep(5)
            self.driver.find_element("xpath","//select[@id='ctl00_ContentPlaceHolder1_gvResults_ctl01_PageSizeDropDownTop']").click()
            self.driver.find_element("xpath","//select[@id='ctl00_ContentPlaceHolder1_gvResults_ctl01_PageSizeDropDownTop']/option[@value='100']").click()
            self.driver.find_element("xpath","(//input[@value='Select'])[1]").click()
            sleep(3)
        except:
            pass
        all = self.driver.find_elements("xpath","//li[contains(@id,'ctl00_ContentPlaceHolder1_liPlanning2ndLevel')]/a")

        for i in all:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", i)
                self.driver.execute_script("arguments[0].click();", i)
            except:
                self.driver.find_element("xpath","//li[contains(@id,'ctl00_ContentPlaceHolder1_liPlanning2ndLevel3')]/a").click()



            page = self.driver.page_source
            html = Selector(text=page)
            links = html.xpath("//td[@class=' datecolumn']/a/@href").getall()
            self.listhref.extend(links)
            
            last = html.xpath("(//li[a/text()='Next'])[1]/preceding-sibling::li/a/text()").getall()
            lastt = int(last[-1])

            start = 1
            while start < lastt:
                try:
                    self.driver.find_element('xpath',"(//a[text()='Next'])[1]").click()

                    page = self.driver.page_source
                    html = Selector(text=page)
                    links = html.xpath("//td[@class=' datecolumn']/a/@href").getall()
                    self.listhref.extend(links)
                    
                except:
                    break
                start += 1

                
        for x in self.listhref:
            yield scrapy.Request(url=x,callback=self.each)

    

    def each(self,response):
        each = {}
        row = response.xpath("//th[@scope='row']")
        for i in row:
            head = i.xpath(".//p/text()").get()
            body = i.xpath(".//following-sibling::td/descendant::text()").getall()
            bodyall = ''.join(body)
            bodyall = bodyall.replace('\r','').replace('\n','').replace('\t','').strip()

            fir = camel_case(head)

            each[fir] = bodyall
        yield each
        self.total.append(each)
        

    def spider_closed(self, spider):
        self.driver.close()
        spider.logger.info("Spider closed: %s", spider.name)
        