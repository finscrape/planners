import scrapy
from planners.util import dates_strxx
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



class ShollandSpider(scrapy.Spider):
    name = "sholland"
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
        start = 0
        for d in dates_strxx[0:-1]:
            start += 1
            fd = d
            nd = dates_strxx[start]

            self.driver.get("https://planning.sholland.gov.uk/OcellaWeb/planningSearch")
            sleep(2)
            try:
            #date picker
                fromDate = self.driver.find_element("xpath","//input[@id='receivedFrom']")

                fromDate.clear()

                fromDate.send_keys(fd)

                fromto = self.driver.find_element("xpath","//input[@id='receivedTo']")
                fromto.clear()

                fromto.send_keys(nd)

                
            except:
                continue

            try:
                self.driver.find_element('xpath',"//input[@value='Search']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//input[@value='Search']").click()
                except:
                    continue
            
            try:
                self.driver.find_element('xpath',"//input[@value='Show all results']").click()
            except:
                pass

            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//table/descendant::a/@href").getall()
            print(f'Date search------{fd}------{nd}')
            print(f'Date search------{fd}------{nd}')
            print(f'Date search------{fd}------{nd}')
            print(f'Date search------{fd}------{nd}')
            print(f'Date search------{fd}------{nd}')
            if links:
                self.listhref.extend(links)
            else:
                continue
        
        for i in self.listhref:
                
                abs_i = f'https://planning.sholland.gov.uk/OcellaWeb/{i}'
                self.drivera.get(abs_i)

                sleep(2)
                pagey = self.drivera.page_source
                htmla = Selector(text=pagey)
                    
                
                each = {}

                each['planningUrl'] = self.drivera.current_url
                table_hd = htmla.xpath("//table[2]/descendant::tr/td[1]")
                for i in table_hd:
                    first = i.xpath(".//descendant::text()").get()
                    second = i.xpath(".//following-sibling::td/descendant::text()").get()
                    if second:
                        
                        second = stripper(second)

                    try:
                        fir = camel_case(first)

                        each[fir] = second
                    except:
                        each[first] = second
                try:
            
                    self.drivera.find_element('xpath',"//input[@value='View Documents']").click()
                    sleep(2)

                    page = self.drivera.page_source
                    html = Selector(text=page)

                    head = html.xpath("//strong")
                    for h in head[1:]:
                        hdtext = h.xpath(".//text()").get()
                        rd = h.xpath(".//following-sibling::table[1]/descendant::tr")

                        chlink = h.xpath(".//following-sibling::table[1]/descendant::tr/td[1]/a/@href").getall()
                        if chlink:
                            doc_doc = []
                            for i in rd:
                                li = stripper(i.xpath(".//td[1]/a/@href").get())
                                if li:
                                    e_rel={}
                                    e_rel['documentName'] = stripper(i.xpath(".//td[1]/a/descendant::text()").get())
                                    e_rel['date'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                                    e_rel['documentLink'] = 'https://planning.sholland.gov.uk/OcellaWeb/' + li
                                    doc_doc.append(e_rel)
                        else:
                            doc_doc = ""
                        
                        each[hdtext] = doc_doc
                except:
                    pass
                yield each
                    

    
                self.total.append(each)
                    
    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()
        
        spider.logger.info("Spider closed: %s", spider.name)
    

                            

