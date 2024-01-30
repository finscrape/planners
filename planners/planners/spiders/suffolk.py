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
global drivera
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


class SuffolkSpider(scrapy.Spider):
    name = "suffolk"
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
            
            self.driver.get("http://suffolk.planning-register.co.uk/Disclaimer?returnUrl=%2FSearch%2FResults")
            sleep(5)
            try:

                searchPl = self.driver.find_element('xpath',"//input[@value='Accept']")
                self.driver.execute_script("arguments[0].scrollIntoView();", searchPl)
                self.driver.execute_script("arguments[0].click();", searchPl)
            except:
                 pass
            
            sleep(5)
            try:
                searchPl = self.driver.find_element('xpath',"//a[text()='View all planning applications']")
                self.driver.execute_script("arguments[0].scrollIntoView();", searchPl)
                self.driver.execute_script("arguments[0].click();", searchPl)
            except:
                pass
            
            page = self.driver.page_source
            html = Selector(text=page)
            sleep(3)

            links = html.xpath("//tr/td/a[@class='large']/@href").getall()
            self.listhref.extend(links)

            
            num =1
            while True:
                num += 1
                try:
                    nextPl = self.driver.find_element('xpath',"(//a[text()='Next'])[1]")
                    self.driver.execute_script("arguments[0].scrollIntoView();", nextPl)
                    self.driver.execute_script("arguments[0].click();", nextPl)
                    sleep(2)

                    page = self.driver.page_source
                    html = Selector(text=page)

                    links = html.xpath("//tr/td/a[@class='large']/@href").getall()
                    self.listhref.extend(links)
                    print(f'{num} planning pages')
                    print(f'{num} planning pages')
                    print(f'{num} planning pages')
                    print(f'{num} planning pages')

                except:
                    break
            
                

            
            for i in self.listhref:
                abs_i = f'http://suffolk.planning-register.co.uk{i}'
                
                self.drivera.get(abs_i)
                sleep(1)
                try:

                    searchPl = self.drivera.find_element('xpath',"//input[@value='Accept']")
                    self.drivera.execute_script("arguments[0].scrollIntoView();", searchPl)
                    self.drivera.execute_script("arguments[0].click();", searchPl)

                except:
                        pass
                sleep(2)
                page = self.drivera.page_source
                html = Selector(text=page)
                
                
                
                each = {}
                each['planningUrl'] = self.drivera.current_url

                box = html.xpath("//label")
                for i in box:
                    table_hd = i.xpath(".//text()").get()
                    table_hd = table_hd.replace("'",'')
                    
                    second = i.xpath(".//following-sibling::div/descendant::text()").getall()
                    allsecond = ''.join(second)
                    allsecond = allsecond.replace('\r','').replace('\n','').replace('\t','').strip()


                    fir = camel_case(table_hd)

                    each[fir] = allsecond

                
                    fir = camel_case(table_hd)

                    each[fir] = allsecond

                nei_doc = []
                rd = html.xpath("//table[@class='col-xs-12']/descendant::tr")
                for i in rd[1:]:
                    e_rel={}
                    e_rel['consulteeName'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                    e_rel['dateLetterSent'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                    e_rel['consultationExpiryDate'] = stripper(i.xpath(".//td[3]/descendant::a/@href").get())
                    e_rel['replyReceived'] = stripper(i.xpath(".//td[3]/descendant::a/@href").get())
                    nei_doc.append(e_rel)
                if nei_doc:
                    each['consultees'] = nei_doc

                doc_doc = []
                rd = html.xpath("//table[@id='documentsdata']/descendant::tr")
                for i in rd[1:]:
                    e_rel={}
                    e_rel['description'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                    e_rel['created'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                    alink = stripper(i.xpath(".//td[2]/descendant::a/@href").get())
                    if alink:
                        e_rel['download'] = 'https://suffolk.planning-register.co.uk' + alink
                        doc_doc.append(e_rel)
                
                if doc_doc:
                    each['documents'] = doc_doc
                
                yield each
                self.total.append(each)
                

            
    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()

        spider.logger.info("Spider closed: %s", spider.name)
    