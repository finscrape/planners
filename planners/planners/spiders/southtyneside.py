import scrapy
from typing import Iterable
import scrapy
from scrapy.http import Request
import scrapy
from planners.util import dates_str
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
import requests
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

class SouthtynesideSpider(scrapy.Spider):
    name = "southtyneside"
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

        

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(url="http://planning.southtyneside.info/Northgate/PlanningExplorer/GeneralSearch.aspx")
    def parse(self, response):

        allwards = response.xpath("//select[@id='cboWardCode']/option").getall()
        each = 0
        for x in allwards[1:]:
            each += 1

            self.driver.get("http://planning.southtyneside.info/Northgate/PlanningExplorer/GeneralSearch.aspx")           
            
            try:
                self.driver.find_element('xpath',"(//a[@title='Allow All Cookies'])[1]").click()
            except:
                pass

            
            try:
                self.driver.find_element('xpath',"(//a[@title='Allow All Cookies'])[1]").click()
            except:
                try:
                    self.driver.find_element('xpath',"(//a[@title='Allow All Cookies'])[1]").click()
                except:
                    pass


            self.driver.find_element('xpath',"//select[@id='cboWardCode']").click()
            
            all = self.driver.find_elements('xpath',"//select[@id='cboWardCode']/option")
            all[each].click()
            

            self.driver.find_element('xpath',"//input[@id='csbtnSearch']").click()

            page = self.driver.page_source
            html = Selector(text=page)

            links = html.xpath("//td[@title='View Application Details']/a/@href").getall()
            self.listhref.extend(links)

            while True:
                try:
                    self.driver.find_element("xpath","//a[img/@alt='Go to next page ']").click()
                    sleep(2)
                    page = self.driver.page_source
                    html = Selector(text=page)
                    links = html.xpath("//td[@title='View Application Details']/a/@href").getall()
                    self.listhref.extend(links)
                    xl = len(self.listhref)

                    print(f'Gathered {xl} planning apps')
                    print(f'Gathered {xl} planning apps')
                    print(f'Gathered {xl} planning apps')
                    print(f'Gathered {xl} planning apps')
                    
                except:
                    break
        
        
        #using driver to stabilze planning page
        self.drivera.get("https://planning.southtyneside.info/Northgate/PlanningExplorer/GeneralSearch.aspx")
        try:
            self.drivera.find_element('xpath',"(//a[@title='Allow All Cookies'])[1]").click()
        except:
            try:
                self.drivera.find_element('xpath',"(//a[@title='Allow All Cookies'])[1]").click()
            except:
                pass
        sleep(2)
        self.drivera.find_element('xpath',"//select[@id='cboWardCode']").click()
            
        all = self.drivera.find_elements('xpath',"//select[@id='cboWardCode']/option")
        all[-1].click()
        

        self.drivera.find_element('xpath',"//input[@id='csbtnSearch']").click()

        sleep(5)
        for i in self.listhref:
            i = stripper(i)
            ispl = i.split(" ")
            newi = '%20'.join(ispl)
            
            abs_i = f'https://planning.southtyneside.info/Northgate/PlanningExplorer/Generic/{newi}'
            
            self.drivera.get(abs_i)
            sleep(1)

            try:
                self.drivera.find_element('xpath',"(//a[@title='Allow All Cookies'])[1]").click()
            except:
                try:
                    self.drivera.find_element('xpath',"(//a[@title='Allow All Cookies'])[1]").click()
                except:
                    pass

            page = self.drivera.page_source
            html = Selector(text=page)


            each = {}
            each['planningUrl'] = abs_i
            box = html.xpath("//div/span")
            for i in box:
                table_hd = i.xpath(".//text()").get()
                table_hd = stripper(table_hd)
                second = i.xpath(".//following-sibling::text()").getall()
                allsecond = ''.join(second)
                allsecond = stripper(allsecond)
                try:
                    fir = camel_case(table_hd)

                    each[fir] = allsecond
                except:
                    each[table_hd] = allsecond

            
            olinks = html.xpath("(//a[contains(@title,'Dates page')]/@href | //a[contains(@title,'related documents')]/@href)").getall()
            for a in olinks:
                abs_a = f'http://planning.southtyneside.info/Northgate/PlanningExplorer/Generic/{a}'
                
                self.drivera.get(abs_a)
                page = self.drivera.page_source
                html = Selector(text=page)

                box = html.xpath("//div/span")
                if box:
                    for i in box:
                        table_hd = i.xpath(".//text()").get()
                        table_hd = stripper(table_hd)
                        second = i.xpath(".//following-sibling::text()").getall()
                        allsecond = ''.join(second)
                        allsecond = stripper(allsecond)
                        try:
                            fir = camel_case(table_hd)

                            each[fir] = allsecond
                        except:
                            each[table_hd] = allsecond


            yield each
            self.total.append(each)
            
    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()

        spider.logger.info("Spider closed: %s", spider.name)
    