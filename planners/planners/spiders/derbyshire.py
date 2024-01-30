import scrapy
from planners.util import dates_str5
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




class DerbyshireSpider(scrapy.Spider):
    name = "derbyshire"
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
        self.driver.get('https://planning.derbyshire.gov.uk/Search/Advanced?Length=6')
        sleep(3)

        try:
            self.driver.find_element("xpath","//button[text()='Close']").click()
        except:
            try:
                self.driver.find_element("xpath","//button[text()='Close']").click()
            except:
                pass
        sleep(3)
        try:
            self.driver.find_element("xpath","//input[@id='submitDisclaimer']").click()
        except:
            try:
                self.driver.find_element("xpath","//input[@id='submitDisclaimer']").click()
            except:
                pass
        sleep(3)

        try:
            self.driver.find_element("xpath","//input[@value='Search']").click()
        except:
            try:
                self.driver.find_element("xpath","//input[@value='Search']").click()
            except:
                pass
        sleep(3)

        page = self.driver.page_source
        html = Selector(text=page)

        links = html.xpath("//div/span/a[contains(@href,'Display')]/@href").getall()
        for i in links:
            abs_i  =f'https://planning.derbyshire.gov.uk{i}'
            self.listhref.append(abs_i)

        x = 1
        while True:
            try:
                nextPl = self.driver.find_element('xpath',"(//a[text()='Next'])[1]")
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

                links = html.xpath("//div/span/a[contains(@href,'Display')]/@href").getall()
                for i in links:
                    abs_i  =f'https://planning.derbyshire.gov.uk{i}'
                    self.listhref.append(abs_i)
                break

            except:
                break


        self.drivera.get('https://planning.derbyshire.gov.uk/Search/Advanced?Length=6')
        sleep(3)

        try:
            self.drivera.find_element("xpath","//button[text()='Close']").click()
        except:
            try:
                self.drivera.find_element("xpath","//button[text()='Close']").click()
            except:
                pass
        sleep(3)
        try:
            self.drivera.find_element("xpath","//input[@id='submitDisclaimer']").click()
        except:
            try:
                self.drivera.find_element("xpath","//input[@id='submitDisclaimer']").click()
            except:
                pass
        sleep(3)

        try:
            self.drivera.find_element("xpath","//input[@value='Search']").click()
        except:
            try:
                self.drivera.find_element("xpath","//input[@value='Search']").click()
            except:
                pass
        sleep(3)
        
        for ai in self.listhref[0:3]:
            self.drivera.get(ai)
            sleep(2)
            page = self.drivera.page_source
            html = Selector(text=page)

            
            each = {}
            each['planningUrl'] = ai

            box = html.xpath("//li[@class='row']/label")
            for i in box:
                table_hd = i.xpath(".//text()").get()
                table_hd = stripper(table_hd)
                second = i.xpath(".//following-sibling::div[1]/span/input/@value").getall()
                if not second:
                    second = i.xpath(".//following-sibling::div[1]/span/textarea/text()").getall()
                allsecond = ''.join(second)
                allsecond = stripper(allsecond)
                try:
                    fir = camel_case(table_hd)

                    each[fir] = allsecond
                except:
                    each[table_hd] = allsecond

            #consultees
            box2  = html.xpath("//table[@summary='Consultees table']/descendant::tr")
            hd = box2.xpath(".//th/descendant::text()").getall()
            hd = [camel_case(i) for i in hd]
            con_doc = []
            if box2:
                for i in box2:
                    bd = i.xpath(".//descendant::td/descendant::text()").getall()
                    if bd:
                        x = 0
                        e_rel = {}
                        for ii in bd:
                            
                            hed = hd[x]
                            e_rel[hed] = ii
                            x+=1
                        con_doc.append(e_rel)
                    each['consultees'] = con_doc

             #constraint
            box3  = html.xpath("//div[@id='constraintsTab']/descendant::table/descendant::tr")
            hd = box3.xpath(".//th/descendant::text()").getall()
            hd = [camel_case(i) for i in hd]
            con_doc = []
            if box3:
                for i in box3:
                    bd = i.xpath(".//descendant::td/descendant::text()").getall()
                    if bd:
                        x = 0
                        e_rel = {}
                        for ii in bd:
                            
                            hed = hd[x]
                            e_rel[hed] = ii
                            x+=1
                        con_doc.append(e_rel)
                    each['constraints'] = con_doc

            #documents
            doc_doc = []
            box5 = html.xpath("//table[@summary='Planning document grid']/descendant::tr")
            if box5:
                for i in box5[2:]:
                    e_rel={}
                    l = stripper(i.xpath(".//td[2]/descendant::a/@href").get())
                    if l:
                        e_rel['fileLink'] = 'https://planning.derbyshire.gov.uk' + l
                    
                        e_rel['fileName'] = stripper(i.xpath(".//td[2]/descendant::a/text()").get())
                        e_rel['description'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                        e_rel['dateUploaded'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                        doc_doc.append(e_rel)
                    
                each['documents'] = doc_doc


            yield each


    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()

        spider.logger.info("Spider closed: %s", spider.name)
    