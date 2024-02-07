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



class RochfordSpider(scrapy.Spider):
    name = "rochford"
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
        yield scrapy.Request(url='https://maps.rochford.gov.uk/DevelopmentControl.aspx?RequestType=ParseTemplate&template=DevelopmentControlAdvancedSearch.tmplt')

    def parse(self, response):

        

        allwards = response.xpath("//select[@id='srchParish']/option/@value").getall()
        each = 1

        for x in allwards[1:]:
            
            fd = "01/01/1900"
            nd = "01/01/2024"
            self.driver.get('https://maps.rochford.gov.uk/DevelopmentControl.aspx?RequestType=ParseTemplate&template=DevelopmentControlAdvancedSearch.tmplt')

            try:
                self.driver.find_element('xpath',"(//a[@title='Allow All Cookies'])[1]").click()
            except:
                pass

            
            try:
                self.driver.find_element('xpath',"(//a[@title='Allow All Cookies'])[1]").click()
            except:
                pass
            sleep(3)
            self.driver.find_element('xpath',"//select[@id='srchParish']").click()
            
            all = self.driver.find_elements('xpath',"//select[@id='srchParish']/option")

            try:
                all[each].click()
            except:
                pass


            
            each+= 1

            #date picker
            fromDate = self.driver.find_element("xpath","//input[@id='dateaprecvfrom']")

            fromDate.clear()

            fromDate.send_keys(fd)

            fromto = self.driver.find_element("xpath","//input[@id='dateaprecvto']")
            fromto.clear()

            fromto.send_keys(nd)


            

            searchPl = self.driver.find_element('xpath',"//button[@id='submit-advanced']")
            self.driver.execute_script("arguments[0].scrollIntoView();", searchPl)
            self.driver.execute_script("arguments[0].click();", searchPl)
            sleep(5)
            

            cl = self.driver.current_url
            self.driver.get(cl)
            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//div[@id='results']/descendant::dt/a/@href").getall()
            self.listhref.extend(links)


            
            #Sfinding next link

        
            while True:
                try:
                    self.driver.find_element("xpath","//li[@class='next']/a").click()
                    sleep(2)
                    page = self.driver.page_source
                    html = Selector(text=page)
                    links = html.xpath("//div[@id='results']/descendant::dt/a/@href").getall()
                    self.listhref.extend(links)

                    xlen = len(self.listhref)
                    print(f'{xlen} planning applications')
                    print(f'{xlen} planning applications')
                    print(f'{xlen} planning applications')
                    print(f'{xlen} planning applications')
                    
                except:
                    break
    
            
            

        
            
                
            
        for i in self.listhref:
            self.drivera.get(i)
            sleep(1)

            page = self.drivera.page_source
            html = Selector(text=page)
            each = {}
            each['planningUrl'] = self.drivera.current_url

            links = html.xpath("//ul[@class='tabs sub-tabs']/li/a/@href").getall()
            for i in links[:-1]:
                abs_i =f'https://maps.rochford.gov.uk/DevelopmentControl.aspx{i}'
                self.drivera.get(abs_i)
                sleep(2)

                page = self.drivera.page_source
                html = Selector(text=page)
            
                table_hd = html.xpath("//dl/dt")
                for i in table_hd:
                    first = i.xpath(".//text()").get()
                    second = i.xpath(".//following-sibling::dd/text()").getall()
                    if second:
                        second = ''.join(second)
                        second = stripper(second)
                    else:
                        second = ""

                    try:
                        fir = camel_case(first)

                        each[fir] = second
                    except:
                        each[fir] = second

            yield each
    
    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()
        spider.logger.info("Spider closed: %s", spider.name)
            
