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


class CivicacxSpider(scrapy.Spider):
    name = "civicacx"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = 0
        self.total = []
        self.driver = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
        self.driver.maximize_window()

        

        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self, response):
        start = 0
        
        
        for d in dates_strx[0:-1]:

            start += 1
            fd = d
            ffd = fd.split("/")
            
            ffd = ffd[-1]
            ffd = int(ffd)
            if ffd < 2006:
                print('Too old to search from')
                continue

            nd = dates_strx[start]
        
            self.driver.get("https://register.civicacx.co.uk/Erewash/Planning/Search/BackToSearch?pcid=f594afa8-8d2a-4db9-a4a3-e8caca53d781")
            sleep(3)
            

            try:
                #date picker
                fromDate = self.driver.find_element("xpath","//input[@id='DateValidFrom']")

                fromDate.clear()

                fromDate.send_keys(fd)

                fromto = self.driver.find_element("xpath","//input[@id='DateValidTo']")
                fromto.clear()

                fromto.send_keys(nd)
            except:
                pass

            

            sleep(1)
            try:
                self.driver.find_element('xpath',"//button[@value='SearchAll']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//button[@value='SearchAll']").click()
                except:
                    pass
            sleep(2)
            
            

            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//a[contains(text(),'Details')]/@href").getall()
            if not links:
                continue
            
            self.listhref.extend(links)

            x = 0
            while True:
                
                
                try:
                    searchPl = self.driver.find_element("xpath","//a[contains(@aria-label,'Next') and @href != '#']")
                    self.driver.execute_script("arguments[0].scrollIntoView();", searchPl)
                    self.driver.execute_script("arguments[0].click();", searchPl)
                    
                    sleep(1)
                    pagex = self.driver.page_source
                    html = Selector(text=pagex)
                    links = html.xpath("//a[contains(text(),'Details')]/@href").getall()
                    if not links:
                        continue
                    x += 1
                    self.listhref.extend(links)

                    print(f'From  -----getting the {x} pageeee')
                    print(f'From ------getting the {x} pageeee')
                    print(f'From ------getting the {x} pageeee')
                    

                    
                except:
                    break

        for i in self.listhref:
            ai = f'https://register.civicacx.co.uk{i}'
            yield scrapy.Request(url=ai,callback=self.details)
    def details(self,response):        
            
            
            each = {}
            each['planningUrl'] = response.url

            box = response.xpath("//dt")
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

            doc_li = response.url.replace('DetailsPage','DocumentsPage')
            if doc_li:
                
                yield scrapy.Request(url=doc_li,callback=self.docs,meta={'each':each})
            else:
                yield each
    
    def docs(self,response):
        #documents
        each = response.meta['each']
        box2  = response.xpath("//table/descendant::tr")
        if box2:
            con_doc = []
            for i in box2[1:]:
                try:
                    e_rel={}
                    l = stripper(i.xpath(".//td[3]/descendant::a/@href").get())
                    if l:

                        e_rel['documentLink'] = 'https://register.civicacx.co.uk'+l
                        e_rel['documentType'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                        e_rel['documentName'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                            
                        con_doc.append(e_rel)
                except:
                    pass
            each['allDocuments'] = con_doc

        yield each

    def spider_closed(self, spider):
        self.driver.quit()
        spider.logger.info("Spider closed: %s", spider.name)
      
