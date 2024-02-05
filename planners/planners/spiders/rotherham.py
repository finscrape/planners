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

class RotherhamSpider(scrapy.Spider):
    name = "rotherham"
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
        
        for d in dates_strx[0:-1]:

            start += 1
            fd = d
            ffd = fd.split("/")
            
            ffd = ffd[-1]
            ffd = int(ffd)
            if ffd < 1945:
                print('Too old to search from')
                continue

            nd = dates_strx[start]
            self.driver.get("https://planning.rotherham.gov.uk/search.asp")
            sleep(3)

            try:
                #date picker
                fromDate = self.driver.find_element("xpath","//input[@name='DateReceivedStart']")

                fromDate.clear()

                fromDate.send_keys(fd)

                fromto = self.driver.find_element("xpath","//input[@name='DateReceivedEnd']")
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
            
            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//a[text()='View Details']/@href").getall()
            if not links:
                continue
            self.listhref.extend(links)
            print('Date search')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')


            x = 0
            while True:
                x += 1
              
                try:
                    searchPl = self.driver.find_element("xpath","//a[text()='Next']")
                    self.driver.execute_script("arguments[0].scrollIntoView();", searchPl)
                    self.driver.execute_script("arguments[0].click();", searchPl)
                    
                    sleep(3)
                    pagex = self.driver.page_source
                    html = Selector(text=pagex)
                    links = html.xpath("//a[text()='View Details']/@href").getall()
                    if not links:
                        continue
                    self.listhref.extend(links)
                    print(f'From {fd} to {nd}------getting the {x} pageeee')
                    print(f'From {fd} to {nd}------getting the {x} pageeee')
                    print(f'From {fd} to {nd}------getting the {x} pageeee')
                    
                    
                    
                except:
                    break
        
        for i in self.listhref:
            
            abs_i = f'https://planning.rotherham.gov.uk/{i}'
            try:
                self.drivera.get(abs_i)
                sleep(2)
            except:
                try:
                    self.drivera.get(abs_i)
                    sleep(2)
                except:
                    continue
                
            page = self.drivera.page_source
            html = Selector(text=page)

            
            each = {}
            each['planningUrl'] = abs_i
            box = html.xpath("//th[@class='RecordTitle']")
            id = html.xpath("//th[contains(text(),'Planning Application Number:')]/following-sibling::td/text()").get()
            for i in box:
                table_hd = i.xpath(".//descendant::text()").get()
                table_hd = stripper(table_hd)
                second = i.xpath(".//following-sibling::*[1]/descendant::text()").getall()
                
                allsecond = ''.join(second)
                allsecond = stripper(allsecond)
                try:
                    fir = camel_case(table_hd)

                    each[fir] = allsecond
                except:
                    each[table_hd] = allsecond

            dec_prog = html.xpath("//a[contains(text(),'Summary')]/@href | //a[contains(text(),'Details')]/@href").getall()
            doc_li = f'https://rotherham.planportal.co.uk/?id={id}'
            
            for i in dec_prog:
                abs_i = f'https://planning.rotherham.gov.uk/{i}'
                self.drivera.get(abs_i)
                sleep(1)
                page = self.drivera.page_source
                html = Selector(text=page)

                
                box = html.xpath("//th[@class='RecordTitle']")
                for i in box:
                    table_hd = i.xpath(".//descendant::text()").get()
                    table_hd = stripper(table_hd)
                    second = i.xpath(".//following-sibling::*[1]/descendant::text()").getall()
                    
                    allsecond = ''.join(second)
                    allsecond = stripper(allsecond)
                    try:
                        fir = camel_case(table_hd)

                        each[fir] = allsecond
                    except:
                        each[table_hd] = allsecond

            #documents
            self.drivera.get(doc_li)
            sleep(1)
            page = self.drivera.page_source
            html = Selector(text=page)

            
            box = html.xpath("//table[contains(@id,'gridview-')]/descendant::tr")
            if box:
                doc_doc = []
                for i in box:
                    e_rel={}
                    e_rel['description'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                    e_rel['fileType'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                    e_rel['fileSize'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                    e_rel['datePublished'] = stripper(i.xpath(".//td[5]/descendant::text()").get())
                    doc_doc.append(e_rel)
                
                each['documents'] = doc_doc

            yield each

    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()

        spider.logger.info("Spider closed: %s", spider.name)
    