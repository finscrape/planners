import scrapy
from planners.util import dates_str5
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver

options = FirefoxOptions()
# options.add_argument("--headless")
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




class WesthatSpider(scrapy.Spider):
    name = "westHat"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = 0
        self.total = []
        self.driver = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
        self.driver.maximize_window()

        # dispatcher.connect(self.spider_closed,signals.spider_closed)

    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self, response):
        self.driver.get('https://planning.welhat.gov.uk/Search/Advanced')
        sleep(2)

        try:
            self.driver.find_element("xpath","//input[@id='SearchPlanning']").click()
        except:
            try:
                self.driver.find_element("xpath","//input[@id='SearchPlanning']").click()
            except:
                pass

        try:
            searchPl = self.driver.find_element('xpath',"(//input[2])[2]")
            self.driver.execute_script("arguments[0].scrollIntoView();", searchPl)
            self.driver.execute_script("arguments[0].click();", searchPl)
        except:
            pass
            
        sleep(2)


        page = self.driver.page_source
        html = Selector(text=page)

        links = html.xpath("//div[@class='item__title']/a/@href").getall()
        for i in links:
            abs_i  =f'https://planning.welhat.gov.uk/{i}'
            self.listhref.append(abs_i)

        x = 1
        while True:
            try:
                nextPl = self.driver.find_element('xpath',"(//a[text()='Next'])[1]")
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

                links = html.xpath("//div[@class='item__title']/a/@href").getall()
                for i in links:
                    abs_i  =f'https://planning.welhat.gov.uk/{i}'
                    self.listhref.append(abs_i)
                break
            except:
                break

        
        for i in self.listhref[0:3]:
            yield scrapy.Request(url=i,callback=self.last)

    def last(self,response):
        each = {}
        each['planningUrl'] = response.url
        box1 = response.xpath("(//div[@class='icmform'])[1]/table/descendant::tr/td")
        box2 = response.xpath("(//div[@class='icmform'])[2]/table/descendant::tr")
        box3 = response.xpath("(//div[@class='icmform'])[3]/table/descendant::tr")
        box4 = response.xpath("(//div[@class='icmform'])[4]/table/descendant::tr/td")
        box5 = response.xpath("(//div[@class='icmform'])[5]/table/descendant::tr")
        box6 = response.xpath("(//div[@class='icmform'])[6]/table/descendant::tr")
        box7 = response.xpath("(//div[@class='icmform'])[7]/table/descendant::tr")
        box8 = response.xpath("(//div[@class='icmform'])[8]/table/descendant::tr")

                    



        for i in box1:
            table_hd = i.xpath(".//descendant::label/text()").get()
            table_hd = table_hd.replace("'",'')
            table_hd = stripper(table_hd)
            
            second = i.xpath(".//descendant::label/following-sibling::div/descendant::text()").getall()
            if second:
                allsecond = ''.join(second)
                allsecond = stripper(allsecond)

            try:
                fir = camel_case(table_hd)

                each[fir] = allsecond
            except:
                each[table_hd] = allsecond

        for i in box4:
            table_hd = i.xpath(".//descendant::label/text()").get()
            table_hd = table_hd.replace("'",'')
            table_hd = stripper(table_hd)
            
            second = i.xpath(".//descendant::label/following-sibling::div/descendant::text()").getall()
            if second:
                allsecond = ''.join(second)
                allsecond = stripper(allsecond)

            try:
                fir = camel_case(table_hd)

                each[fir] = allsecond
            except:
                each[table_hd] = allsecond
        
        #constraints
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
                each['constraint'] = con_doc

        #consultees
        hd = box6.xpath(".//th/descendant::text()").getall()
        hd = [camel_case(i) for i in hd]
        con_doc = []
        if box6:
            for i in box6:
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

        #neighbour
        hd = box7.xpath(".//th/descendant::text()").getall()
        hd = [camel_case(i) for i in hd]
        con_doc = []
        if box7:
            for i in box7:
                bd = i.xpath(".//descendant::td/descendant::text()").getall()
                if bd:
                    x = 0
                    e_rel = {}
                    for ii in bd:
                        
                        hed = hd[x]
                        e_rel[hed] = ii
                        x+=1
                    con_doc.append(e_rel)
                each['neighbours'] = con_doc

        #history
        
        hd = box8.xpath(".//th/descendant::text()").getall()
        hd = [camel_case(i) for i in hd]
        con_doc = []
        if box8:
            for i in box8:
                bd = i.xpath(".//descendant::td/descendant::text()").getall()
                if bd:
                    x = 0
                    e_rel = {}
                    for ii in bd:
                        
                        hed = hd[x]
                        e_rel[hed] = ii
                        x+=1
                    con_doc.append(e_rel)
                each['history'] = con_doc

        yield each
        self.total.append(each)
        

    def spider_closed(self, spider):
        driver.quit()
        spider.logger.info("Spider closed: %s", spider.name)
            
        
        


