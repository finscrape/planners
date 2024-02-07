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

class SouthhamsSpider(scrapy.Spider):
    name = "southhams"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = 0
        self.total = []
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.driver.maximize_window()

        self.drivera = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
        self.drivera.maximize_window()
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    
    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    
    def parse(self, response):

        self.driver.get('https://southhams.planning-register.co.uk/Disclaimer?returnUrl=%2FSearch%2FAdvanced')
        
        try:
            self.driver.find_element("xpath","//input[@type='checkbox']").click()
            sleep(1)
            self.driver.find_element("xpath","//input[@type='submit']").click()
            
        except:
            pass
        
        sleep(5)

        try:
            self.driver.find_element("xpath","//input[@id='SearchPlanning']").click()
        except:
            try:
                self.driver.find_element("xpath","//input[@id='SearchPlanning']").click()
            except:
                try:
                    self.driver.find_element("xpath","//input[@id='SearchPlanning']").click()
                except:
                    pass
                
        searchPl = self.driver.find_element('xpath',"//button[text()='Search']")
        searchPl.click()
        sleep(100)
        #get planning apllications link
        page = self.driver.page_source
        html = Selector(text=page)
        alinks = html.xpath("//a[contains(@href,'/Planning/Display')]/@href").getall()
        
        self.listhref.extend(alinks)
        last = html.xpath("//li[contains(a/text(),'Next')]/preceding-sibling::li")
        if last:
            lastt = last[-1]
            last_num = lastt.xpath(".//a/text()").get()
            print(f'{last_num}- planning applications')
            print(f'{last_num}- planning applications')
            print(f'{last_num}- planning applications')
            print(f'{last_num}- planning applications')
            num = 1
            while num < int(last_num):
                try:
                    self.driver.find_element('xpath',"//li[contains(a/text(),'Next')]/a").click()
                    sleep(2)
                    page = self.driver.page_source
                    html = Selector(text=page)
                    li = html.xpath("//a[contains(@href,'/Planning/Display')]/@href").getall()
                    self.listhref.extend(li)
                    num+=1
                    
                except:
                    break


    
            for i in self.listhref:
                abs_i = f'https://southhams.planning-register.co.uk{i}'

                self.drivera.get(abs_i)
                try:
                    self.drivera.find_element("xpath","//input[@type='checkbox']").click()
                    sleep(1)
                    self.drivera.find_element("xpath","//input[@type='submit']").click()
                    sleep(5)
                    
                except:
                    pass

                sleep(2)
                page = self.drivera.page_source
                html = Selector(text=page)

                each = {}
                each['planningUrl'] = self.drivera.current_url
                table_hd = html.xpath("//div[@id='MainDetails']/descendant::table[1]/descendant::tr")
                for i in table_hd:
                    first = i.xpath(".//td[1]/text()").get()
                    if first in ['Summary','Important Dates','Further Information','Condition Details / Information Notes']:
                        pass
                    else:
                        second = i.xpath(".//td[1]/following-sibling::td[1]/descendant::text()").getall()
                        second = ''.join(second)
                        second = stripper(second)
                        fir = camel_case(first)

                        each[fir] = second

                table_hd = html.xpath("//div[@id='MainDetails']/descendant::table[2]/descendant::tr")
                for i in table_hd:
                    first = i.xpath(".//td[1]/text()").get()
                    if first in ['Summary','Important Dates','Further Information','Condition Details / Information Notes']:
                        pass
                    else:
                        second = i.xpath(".//td[1]/following-sibling::td[1]/descendant::text()").getall()
                        second = ''.join(second)
                        second = stripper(second)
                        fir = camel_case(first)

                        each[fir] = second

                table_hd = html.xpath("//div[@id='MainDetails']/descendant::table[3]/descendant::tr")
                for i in table_hd:
                    first = i.xpath(".//td[1]/text()").get()
                    if first in ['Summary','Important Dates','Further Information','Condition Details / Information Notes']:
                        pass
                    else:
                        second = i.xpath(".//td[1]/following-sibling::td[1]/descendant::text()").getall()
                        second = ''.join(second)
                        second = stripper(second)
                        fir = camel_case(first)

                        each[fir] = second

                empty = []
                table_hd = html.xpath("//div[@id='MainDetails']/descendant::table[4]/descendant::tr")
                if table_hd:
                    for i in table_hd[1:]:
                        first = i.xpath(".//td/descendant::text()").get()
                        empty.append(first)
                    each['conditionDetailsInformationNotes'] = empty
                        
                yield each
                self.total.append(each)
                

                        

    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()
        spider.logger.info("Spider closed: %s", spider.name)
        
                
