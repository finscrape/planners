import scrapy
from planners.util import dates_str4
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

class KirkleesSpider(scrapy.Spider):
    name = "kirklees"
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
    
        self.driver.get("https://www.kirklees.gov.uk/beta/planning-applications/search-for-planning-applications/default.aspx?advanced_search=true")
        
        #date picker
        sleep(10)
        try:
            self.driver.find_element('xpath',"//input[@value='Search']").click()
        except:
            try:
                self.driver.find_element('xpath',"//input[@value='Search']").click()
            except:
                pass
        
        pagex = self.driver.page_source
        html = Selector(text=pagex)
        links = html.xpath("//ul[@class='filter-list']/li/a/@href").getall()
        self.listhref.extend(links)
        print('Date search')
        length = len(self.listhref)
        print(f'{length} planning application')
        print(f'{length} planning application')
        print(f'{length} planning application')
        x = 0
        while True:
            x+=1
            
            try:
                self.driver.find_element("xpath","(//a[contains(text(),'Next ›')])[1]").click()
                sleep(3)
                page = self.driver.page_source
                html = Selector(text=page)

                check = html.xpath("(//a[contains(@disabled,'disabled')])[1]/text()").get()
                if check:
                    break
                links = html.xpath("//ul[@class='filter-list']/li/a/@href").getall()
                
                self.listhref.extend(links)
                length = len(self.listhref)
                print(f'{length} planning application')
                print(f'{length} planning application')
                print(f'{length} planning application')
                
            except:
                break

        
        for i in self.listhref:
            
            abs_i  =f'https://www.kirklees.gov.uk/beta/planning-applications/search-for-planning-applications/{i}'
            self.drivera.get(abs_i)
            sleep(3)

            pagex = self.drivera.page_source
            htmla = Selector(text=pagex)

            each = {}
            url = self.drivera.current_url
            each['planningUrl'] = url
            

            cons_doc = []
            rd = htmla.xpath("//li[@class='doc_list_item']/a[@class='documentTitle']")
            if rd:
                for i in rd:
                    e_rel={}
                    e_rel['name'] = stripper(i.xpath(".//descendant::text()").get())
                    e_rel['description'] = stripper(i.xpath(".//following-sibling::span[2]/descendant::text()").get())
                    e_rel['link'] = 'https://www.kirklees.gov.uk/beta/planning-applications/search-for-planning-applications/' + stripper(i.xpath(".//@href").get())
                    cons_doc.append(e_rel)
            
            
            
            table_hd = htmla.xpath("//dt")
            if table_hd:
                for i in table_hd:
                    first = i.xpath(".//descendant::text()").get()
                    second = i.xpath(".//following-sibling::dd[1]/descendant::text()").getall()
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

            each['documents'] = cons_doc
            yield each
            self.total.append(each)
            
    def spider_closed(self, spider):
        self.driver.quit()
        self.drivera.quit()
        spider.logger.info("Spider closed: %s", spider.name)
                        

                
                        
                        
                        


