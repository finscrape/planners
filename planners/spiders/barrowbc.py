import scrapy
from planners.util import dates_strx
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

class BarrowbcSpider(scrapy.Spider):
    name = "barrowbc"
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
            self.driver.get("https://webapps.barrowbc.gov.uk/webapps/f?p=BARROWPLANNINGHUB:APPLICATIONSEARCH:14514172264224:")
            

            
            sleep(3)
            page = self.driver.page_source
            html = Selector(text=page)

            links = html.xpath("//td[@class=' u-tC']/a/@href").getall()

            for i in links:
                i =i.replace("javascript:apex.navigation.dialog('","")
                i =i.replace(r"\u0026","&")
                i = i.split("',{title:'")
                ii = i[0]
                abs_i  =f'https://webapps.barrowbc.gov.uk/webapps/{ii}'
                self.listhref.append(abs_i)

            x = 1
            while True:
                try:
                    nextPl = self.driver.find_element('xpath',"(//button[@title='Next'])[1]")
                    self.driver.execute_script("arguments[0].scrollIntoView();", nextPl)
                    self.driver.execute_script("arguments[0].click();", nextPl)
                    sleep(2)
                    x += 1
                    print(f'{x} page scraped')
                    print(f'{x} page scraped')
                    print(f'{x} page scraped')
                    print(f'{x} page scraped')
                    
                    page = self.driver.page_source
                    html = Selector(text=page)

                    links = html.xpath("//td[@class=' u-tC']/a/@href").getall()

                    for i in links:
                        i =i.replace("javascript:apex.navigation.dialog('","")
                        i =i.replace(r"\u0026","&")
                        i = i.split("',{title:'")
                        ii = i[0]
                        abs_i  =f'https://webapps.barrowbc.gov.uk/webapps/{ii}'
                        self.listhref.append(abs_i)

                    
                except:
                    break

            
            
            for ai in self.listhref:
                self.driver.get(ai)
                sleep(2)
                page = self.driver.page_source
                html = Selector(text=page)

                
                each = {}

                box = html.xpath("//div[@class='t-Form-labelContainer']/label")
                for i in box:
                    table_hd = i.xpath(".//text()").get()
                    if table_hd:
                        table_hd = stripper(table_hd)
                        second = i.xpath(".//ancestor::div[1]/following-sibling::div[1]/descendant::text()").getall()
                        if second:
                            allsecond = ''.join(second)
                            allsecond = stripper(allsecond)
                        else:
                            allsecond = ""
                        try:
                            fir = camel_case(table_hd)

                            each[fir] = allsecond
                        except:
                            each[table_hd] = allsecond

                box2 = html.xpath("//div[@class='t-Card-info']/a")
                con_doc = []
                if box2:
                   
                    for i in box2:
                        try:
                            e_rel={}
                            
                            e_rel['documentLink'] = stripper(i.xpath(".//@href").get())
                            e_rel['documentTitle'] = stripper(i.xpath(".//ancestor::div[1]/preceding-sibling::div[1]/text()").get())
                                
                            con_doc.append(e_rel)
                        except:
                            pass
                    each['allDocuments'] = con_doc

                each['NeighbourAndConsultees'] = html.xpath("(//div[@class='t-Region-body'])[4]/descendant::div[@class='t-Card-desc']/text()").getall()

                yield each

    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()

        spider.logger.info("Spider closed: %s", spider.name)
    