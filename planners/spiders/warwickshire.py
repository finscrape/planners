import scrapy
from planners.util import dates_str
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from shutil import which
from scrapy_selenium import SeleniumRequest
from time import sleep
from scrapy import Selector
from scrapy import signals


from re import sub
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
global driver

option = webdriver.ChromeOptions()
option.add_argument('--headless=new')
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


class WarwickshireSpider(scrapy.Spider):
    name = "warwickshire"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
        self.driver.maximize_window()

        self.drivera = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
        self.drivera.maximize_window()


        dispatcher.connect(self.spider_closed,signals.spider_closed)

    
    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
        start=0
        for d in dates_str[0:-1]:
                    
                    start += 1
                    fd = d
                    nd = dates_str[start]

                    self.driver.get('https://planning.warwickshire.gov.uk/swiftlg/apas/run/wphappcriteria.display')
        
                    
                    #date picker
                    fromDate = self.driver.find_element("xpath","//input[@id='DateRegisteredFromField']")

                    fromDate.clear()

                    fromDate.send_keys(fd)

                    fromto = self.driver.find_element("xpath","//input[@id='REGTODATE']")
                    fromto.clear()

                    fromto.send_keys(nd)

                    try:
                        self.driver.find_element('xpath',"(//input[@name='SEARCHBUTTON.MAINBODY.WPACIS.1'])[2]").click()
                    except:
                        try:
                            self.driver.find_element('xpath',"(//input[@name='SEARCHBUTTON.MAINBODY.WPACIS.1'])[2]").click()
                        except:
                            pass
                    sleep(2)
                    pagex = self.driver.page_source
                    html = Selector(text=pagex)
                    links = html.xpath("//tr/td/a/@href").getall()
                    self.listhref.extend(links)

                    print(f'From {fd} to {nd}')
                    print(f'From {fd} to {nd}')
                    print(f'From {fd} to {nd}')
                    
                    x = 0
                    while True:
                        x += 1
                        try:
                            next_links = self.driver.find_elements("//div[@class='apas_form_text']/p[2]/a")
                            next_links[x].click()
                            page = self.driver.page_source
                            html = Selector(text=page)
                            links = html.xpath("//tr/td/a/@href").getall()
                            self.listhref.extend(links)
                            print(f'From {fd} to {nd}------getting the {x} pageeee')
                            print(f'From {fd} to {nd}------getting the {x} pageeee')
                            print(f'From {fd} to {nd}------getting the {x} pageeee')

                            
                        except:
                            break

            
        for i in self.listhref:
            abs_i = f'https://planning.warwickshire.gov.uk/swiftlg/apas/run/{i}'
            yield scrapy.Request(url=abs_i,callback=self.parsedetails)

    def parsedetails(self,response):
         each = {}
         table_hd = response.xpath("//span[@class='apas']")
         for i in table_hd:

            first = i.xpath(".//descendant::text()").get()
            second = i.xpath(".//following-sibling::*[1]/descendant::text()").getall()
            if second:
                second = ''.join(second)
                second = stripper(second)

            try:
                fir = camel_case(first)

                each[fir] = second
            except:
                each[first] = second

         con_doc = []
         rd = response.xpath("(//table[@id='tableConsultees'])[1]/descendant::tr")
         if rd:
            for i in rd[1:]:
                e_rel={}
                e_rel['name'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                e_rel['address'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                e_rel['lastLetterDate'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                e_rel['targetResponseDate'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                con_doc.append(e_rel)

         nei_doc = []
         rd = response.xpath("(//table[@id='tableNeighbours'])[1]/descendant::tr")
         if rd:
            for i in rd[1:]:
                e_rel={}
                e_rel['name'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                e_rel['address'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                e_rel['lastLetterDate'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                e_rel['targetResponseDate'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                nei_doc.append(e_rel)


         med_doc = []
         rd = response.xpath("(//table[@id='tableMedia'])[1]/descendant::tr")
         if rd:
            for i in rd[1:]:
                e_rel={}
                e_rel['description'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                e_rel['fileName'] = "https://planning.warwickshire.gov.uk/swiftlg/apas/run/"+stripper(i.xpath(".//td[2]/descendant::a/@href").get())
                med_doc.append(e_rel)


         each['associatedMedia'] = med_doc
         each['consultees'] = con_doc
         each['neighbors'] = nei_doc
         if each:
            yield each
            self.total.append(each)
            
    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()
        spider.logger.info("Spider closed: %s", spider.name)
                        
