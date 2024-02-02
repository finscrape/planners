import scrapy
from planners.util import dates_str6
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


class DudleySpider(scrapy.Spider):
    name = "dudley"
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
        start = 0
        
        
        for d in dates_str6[0:-1]:

            start += 1
            fd = d
            nd = dates_str6[start]

            self.driver.get("https://www5.dudley.gov.uk/swiftlg/apas/run/Wphappcriteria.display")
            sleep(3)

            try:
                #date picker
                fromDate = self.driver.find_element("xpath","//input[@name='REGFROMDATE.MAINBODY.WPACIS.1']")

                fromDate.clear()

                fromDate.send_keys(fd)

                fromto = self.driver.find_element("xpath","//input[@name='REGTODATE.MAINBODY.WPACIS.1']")
                fromto.clear()

                fromto.send_keys(nd)
            except:
                continue

            sleep(1)

            try:
                self.driver.find_element('xpath',"//input[@name='SEARCHBUTTON.MAINBODY.WPACIS.1']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//input[@name='SEARCHBUTTON.MAINBODY.WPACIS.1']").click()
                except:
                    pass
            sleep(3)
            
            

            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//td[@class='apas_tblContent']/a/@href").getall()
            if not links:
                continue
            self.listhref.extend(links)
            print('Date search')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
            
            next_urls = html.xpath("//p[contains(text(),'Pages :')]/a/@href").getall()
            if not next_urls:
                continue
            for i in next_urls:
                abs_i = f'https://www5.dudley.gov.uk/swiftlg/apas/run/{i}'
                self.driver.get(abs_i)
                sleep(2)
                pagex = self.driver.page_source
                html = Selector(text=pagex)
                links = html.xpath("//td[@class='apas_tblContent']/a/@href").getall()
                if not links:
                    continue
                self.listhref.extend(links)
                print('Date search')
                print(f'Next From {fd} to {nd}')
                print(f'Next From {fd} to {nd}')
                print(f'Next From {fd} to {nd}')
        for i in self.listhref:
            ai = f'https://www5.dudley.gov.uk/swiftlg/apas/run/{i}'
            yield scrapy.Request(url=ai,callback=self.details)
    def details(self,response):        
            
            
            each = {}
            each['planningUrl'] = response.url

            box = response.xpath("//span[@class='apas']")
            for i in box:
                table_hd = i.xpath(".//descendant::text()").get()
                if table_hd:
                    table_hd = stripper(table_hd)
                    second = i.xpath(".//following-sibling::p[@class='fieldset_data'][1]/descendant::text()").getall()
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

            doc_li = response.xpath("//h2[text()='Associated Media']/following-sibling::a/@href").get()
            if doc_li:
                yield scrapy.Request(url=doc_li,callback=self.docs,meta={'each':each})
            else:
                yield each
    
    def docs(self,response):
        #documents
        each = response.meta['each']
        box2  = response.xpath("//table[@class='AIMTable']/descendant::tr")
        if box2:
            con_doc = []
            for i in box2[1:]:
                try:
                    e_rel={}
                    l = stripper(i.xpath(".//td[1]/descendant::a/@href").get())
                    if l:

                        e_rel['documentLink'] = 'http://planningdocuments.dudley.gov.uk/AniteIM.WebSearch/(S(qzikue55bewyet55potqa0b4))/'+l
                        e_rel['applicationRef'] = stripper(i.xpath(".//td[1]/descendant::a/text()").get())
                        e_rel['documentDate'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                        e_rel['documentType'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                        e_rel['documentTitle'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                        e_rel['documentNote'] = stripper(i.xpath(".//td[5]/descendant::text()").get())
                            
                        con_doc.append(e_rel)
                except:
                    pass
            each['allDocuments'] = con_doc

        yield each

    def spider_closed(self, spider):
        self.driver.quit()
        self.drivera.quit()
        spider.logger.info("Spider closed: %s", spider.name)
      
