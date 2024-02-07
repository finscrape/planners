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

class GreatYarmouthSpider(scrapy.Spider):
    name = "great-yarmouth"
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
        
        for d in dates_strxx[0:-1]:

            start += 1
            fd = d
            nd = dates_strxx[start]

            self.driver.get("https://planning.great-yarmouth.gov.uk/OcellaWeb/planningSearch")
            sleep(3)

            try:
                #date picker
                fromDate = self.driver.find_element("xpath","//input[@name='receivedFrom']")

                fromDate.clear()

                fromDate.send_keys(fd)

                fromto = self.driver.find_element("xpath","//input[@name='receivedTo']")
                fromto.clear()

                fromto.send_keys(nd)
            except:
                continue

            sleep(1)

            try:
                self.driver.find_element('xpath',"//input[@value='Search']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//input[@value='Search']").click()
                except:
                    pass
            sleep(3)
            
            try:
                self.driver.find_element('xpath',"//input[@value='Show all results']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//input[@value='Show all results']").click()
                except:
                    pass

            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//td/a/@href").getall()
            self.listhref.extend(links)
            print('Date search')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')

        for i in self.listhref:
            ai = f'https://planning.great-yarmouth.gov.uk/OcellaWeb/{i}'
            
            self.drivera.get(ai)

            sleep(2)
            page = self.drivera.page_source
            html = Selector(text=page)

            
            each = {}
            each['planningUrl'] = ai

            box = html.xpath("(//table)[2]/descendant::tr")
            for i in box:
                table_hd = i.xpath(".//td[1]/descendant::text()").get()
                if table_hd:
                    table_hd = stripper(table_hd)
                    second = i.xpath(".//td[2]/descendant::text()").getall()
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
            ref = html.xpath("//td[strong/text()='Reference']/following-sibling::td/text()").get()
            ref_i = f'https://portal.great-yarmouth.gov.uk/planning/search-applications#VIEW?RefType=PLANNINGCASE&KeyText={ref}'
            self.drivera.get(ref_i)
            sleep(2)
            pagex = self.drivera.page_source
            htmlx = Selector(text=pagex)
            
            
            #documents
            box2  = htmlx.xpath("//div[@class='civica-doclist']/ul/li")
            con_doc = []
            if box2:
                
                for i in box2:
                    try:
                        e_rel={}
                        l = stripper(i.xpath(".//a/@href").get())
                        if l:

                            e_rel['fileLink'] = 'https://portal.great-yarmouth.gov.uk/planning/search-applications'+l
                            e_rel['fileName'] = stripper(i.xpath(".//a/descendant::text()").get())
                            e_rel['date'] = stripper(i.xpath(".//div/descendant::text()").get())
                                
                            con_doc.append(e_rel)
                    except:
                        pass
                each['allDocuments'] = con_doc

            


            yield each

    def spider_closed(self, spider):
        self.driver.quit()
        self.drivera.quit()
        spider.logger.info("Spider closed: %s", spider.name)
      