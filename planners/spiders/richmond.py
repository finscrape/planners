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

class RichmondSpider(scrapy.Spider):
    name = "richmond"
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

    def parse(self,response):
        start=0
        for d in dates_str[0:-1]:
            start += 1
            fd = d
            nd = dates_str[start]

            self.driver.get("https://www2.richmond.gov.uk/lbrplanning/Planning_Report.aspx")
        
            sleep(3)
            try:
                self.driver.find_element('xpath',"//button[@id='ccc-recommended-settings']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//button[@id='ccc-recommended-settings']").click()
                except:
                    pass


            
            

            sleep(2)
            #date picker
            fromDate = self.driver.find_element("xpath","//input[@id='ctl00_PageContent_dpValFrom']")

            fromDate.clear()

            fromDate.send_keys(fd)

            fromto = self.driver.find_element("xpath","//input[@id='ctl00_PageContent_dpValTo']")
            fromto.clear()

            fromto.send_keys(nd)


            try:
                self.driver.find_element('xpath',"//select[@id='ctl00_PageContent_ddLimit']").click()
                opt = self.driver.find_elements('xpath',"//select[@id='ctl00_PageContent_ddLimit']/option")
                opt[-1].click()
            except:
                try:
                    self.driver.find_element('xpath',"//select[@id='ctl00_PageContent_ddLimit']").click()
                    opt = self.driver.find_elements('xpath',"//select[@id='ctl00_PageContent_ddLimit']/option")
                    opt[-1].click()
                except:
                    pass

            try:
                self.driver.find_element('xpath',"//input[@value='Search']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//input[@value='Search']").click()
                except:
                    pass
            
            sleep(3)

            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//ul[@class='planning-apps']/descendant::a/@href").getall()
            self.listhref.extend(links)
            
            print(len(self.listhref))
            print(len(self.listhref))
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
            
            
        done_url = []    
        for i in self.listhref:
            
            abs_i = f'https://www2.richmond.gov.uk/lbrplanning/{i}'

            if abs_i not in done_url:
                done_url.append(abs_i)
                yield scrapy.Request(url=abs_i,callback=self.parsedetails)

    def parsedetails(self,response):
        each = {}
        urla = response.url
        each['planningUrl'] = urla
        urlast = urla.split("=")
        each['planningApplication'] = urlast[-1]
        status = response.xpath("//h2[contains(text(),'Status')]/following-sibling::p[1]/descendant::text()").getall()
        astatus = ''.join(status)
        each['status'] = astatus
        each['latest'] = response.xpath("//p[contains(text(),'Latest')]/a/descendant::text()").get()
        each['decisionDue'] = response.xpath("//span[@id='ctl00_PageContent_lbl_Due_Date']/text()").get()
        each['level'] = response.xpath("//span[@id='ctl00_PageContent_lbl_Dec_Level']/text()").get()
        
        table_hd = response.xpath("//div[@class='row']/div[@class='col-sm-8']/h3")
        for i in table_hd:

            first = i.xpath(".//descendant::text()").get()
            if first and first != "  ":
                first = stripper(first)
                second = i.xpath(".//following-sibling::text()").getall()
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

        
        table_sd = response.xpath("//div[@class='row']/div[@class='col-sm-6']/descendant::strong")
        for i in table_sd:

            first = i.xpath(".//descendant::text()").get()
            if first and first != "  ":
                first = stripper(first)
                second = i.xpath(".//following-sibling::text()").getall()
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

        alllinks = response.xpath("//div[@class='lb-list-block-2']/ul/li/a/@href").getall()
        if alllinks:
            alllinks = [f'https://www2.richmond.gov.uk/lbrplanning/{i}' for i in alllinks]
            each['documents'] = alllinks

        if each:
            self.plan +=1
            print(f'{self.plan} planning application')
            print(f'{self.plan} planning application')
            print(f'{self.plan} planning application')
            print(f'{self.plan} planning application')
            yield each
            self.total.append(each)
        
    def spider_closed(self, spider):
        self.driver.quit()
        spider.logger.info("Spider closed: %s", spider.name)
            
