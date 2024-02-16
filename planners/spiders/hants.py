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


class HantsSpider(scrapy.Spider):
    name = "hants"
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
            self.driver.get("https://planning.hants.gov.uk/Disclaimer?returnUrl=%2FSearch%2FStandard%3FQuickSearch%3D")

            try:
                self.driver.find_element('xpath',"//input[@value='Agree']").click()
            except:
                pass
            
            sleep(3)

            page = self.driver.page_source
            html = Selector(text=page)

            links = html.xpath("//td/a/@href").getall()
            for i in links:
                abs_i  =f'https://planning.hants.gov.uk{i}'
                self.listhref.append(abs_i)

            x = 1
            while True:
                try:
                    nextPl = self.driver.find_element('xpath',"(//a[@aria-label='Next Page.'])[1]")
                    self.driver.execute_script("arguments[0].scrollIntoView();", nextPl)
                    self.driver.execute_script("arguments[0].click();", nextPl)
                    sleep(3)
                    x += 1
                    print(f'{x} page scraped')
                    print(f'{x} page scraped')
                    print(f'{x} page scraped')
                    print(f'{x} page scraped')
                    page = self.driver.page_source
                    html = Selector(text=page)

                    page = self.driver.page_source
                    html = Selector(text=page)

                    links = html.xpath("//td/a/@href").getall()
                    for i in links:
                        abs_i  =f'https://planning.hants.gov.uk{i}'
                        self.listhref.append(abs_i)
                    
                    
                except:
                    break

            self.drivera.get("https://planning.hants.gov.uk/Disclaimer?returnUrl=%2FSearch%2FStandard%3FQuickSearch%3D")

            try:
                self.drivera.find_element('xpath',"//input[@value='Agree']").click()
            except:
                pass
            
            sleep(3)


            for ai in self.listhref:
                self.drivera.get(ai)
                sleep(2)
                page = self.drivera.page_source
                html = Selector(text=page)

                
                each = {}
                each['planningUrl'] = ai

                box = html.xpath("//dt")
                for i in box:
                    table_hd = i.xpath(".//descendant::text()").get()
                    if table_hd:
                        table_hd = stripper(table_hd)
                        second = i.xpath(".//following-sibling::dd[1]/descendant::text()").getall()
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

                #neighbours
                box2  = html.xpath("//table[@summary='Planning Document grid']/descendant::tr")
                hd = box2.xpath(".//th/descendant::text()").getall()
                hd = [camel_case(i) for i in hd]
                con_doc = []
                if hd:
                    for i in box2[1:]:
                        try:
                            e_rel={}
                            l = stripper(i.xpath(".//td[2]/descendant::a/@href").get())
                            if l:

                                e_rel['fileLink'] = 'https://planning.hants.gov.uk'+l
                                e_rel['fileName'] = stripper(i.xpath(".//td[2]/descendant::a/text()").get())
                                e_rel['date'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                                    
                                con_doc.append(e_rel)
                        except:
                            pass
                    each['allDocuments'] = con_doc

                yield each
                self.plan+=1
                tot = len(self.listhref)
                print(f"{self.plan} out of {tot}")
                print(f"{self.plan} out of {tot}")
                print(f"{self.plan} out of {tot}")
                

    def spider_closed(self, spider):
        self.driver.quit()
        self.drivera.quit()
        spider.logger.info("Spider closed: %s", spider.name)
      