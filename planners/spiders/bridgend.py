import scrapy
from planners.util import dates_str6
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver

options = FirefoxOptions()
#options.add_argument("--headless")
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


class BridgendSpider(scrapy.Spider):
    name = "bridgend"
    #allowed_domains = ['a.com']
    # start_urls = ['http://a.com/']

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = 0
        self.total = []
        self.driver = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
        self.driver.maximize_window()
        self.drivera = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
        self.drivera.maximize_window()

        # dispatcher.connect(self.spider_closed,signals.spider_closed)

    def start_requests(self):
        yield scrapy.Request(url='https://www.ebay.com',callback=self.parse)
                
    def parse(self,response):

        self.driver.get("https://planning.bridgend.gov.uk/Disclaimer?returnUrl=%2FSearch%2FPlanning%2FAdvanced")

        try:
            self.driver.find_element('xpath',"//input[@value='Agree']").click()
        except:
            pass
        
        sleep(3)

        try:
            self.driver.find_element('xpath',"(//input[@value='Search'])[1]").click()
        except:
            try:
                self.driver.find_element('xpath',"(//input[@value='Search'])[1]").click()
            except:
                pass
        sleep(5)

        page = self.driver.page_source
        html = Selector(text=page)

        links = html.xpath("//td/a/@href").getall()
        for i in links:
            abs_i  =f'https://planning.bridgend.gov.uk{i}'
            self.listhref.append(abs_i)

        x = 1
        last = html.xpath("(//ul[@class='ajax-pager'])[1]/li/a/text()").get()
        lastt =int(last)
        while True:
            if x > lastt:
                break
            try:
                nextPl = self.driver.find_element('xpath',"(//ul[@class='ajax-pager'])[1]/li[@class='active']/following-sibling::li[1]/a")
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
                
                links = html.xpath("//td/a/@href").getall()
                for i in links:
                    abs_i  =f'https://planning.bridgend.gov.uk{i}'
                    self.listhref.append(abs_i)

                break
            except:
                break

        self.drivera.get("https://planning.bridgend.gov.uk/Disclaimer?returnUrl=%2FSearch%2FPlanning%2FAdvanced")

        try:
            self.drivera.find_element('xpath',"//input[@value='Agree']").click()
        except:
            pass
        
        sleep(3)

        try:
            self.drivera.find_element('xpath',"(//input[@value='Search'])[1]").click()
        except:
            try:
                self.drivera.find_element('xpath',"(//input[@value='Search'])[1]").click()
            except:
                pass
        sleep(5)


        for ai in self.listhref:
            self.drivera.get(ai)
            sleep(2)
            page = self.drivera.page_source
            html = Selector(text=page)

            
            each = {}
            each['planningUrl'] = ai

            box = html.xpath("//label[@class='col-sm-3 control-label']")
            for i in box:
                table_hd = i.xpath(".//text()").get()
                if table_hd:
                    table_hd = stripper(table_hd)
                    second = i.xpath("./following-sibling::div[1]/input/@value").getall()
                    if not second:
                        second = i.xpath(".//textarea[1]/text()").getall()
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
            box2  = html.xpath("//div[@id='neighbours']/div[@class='list']")
            hd = box2.xpath(".//div[1]/div/text()").getall()
            hd = [camel_case(i) for i in hd]
            con_doc = []
            if hd:
                box2 = html.xpath("//div[@id='neighbours']/div[@class='list']/div[2]/div")
                for i in box2:
                    bd = i.xpath(".//descendant::div")
                    all = []
                    for b in bd:
                        tx = b.xpath(".//descendant::text()").get()
                        if not tx:
                            tx = ""
                        all.append(tx)
                    if bd:
                        x = 0
                        e_rel = {}
                        for ii in all:
                            
                            hed = hd[x]
                            try:
                                e_rel[hed] = stripper(ii)
                            except:
                                print('Couldnt unpack')
                            x+=1
                        con_doc.append(e_rel)
                    each['neighbours'] = con_doc

            #consultees
            box2  = html.xpath("//div[@id='consultees']/div[@class='list']")
            hd = box2.xpath(".//div[1]/div/text()").getall()
            hd = [camel_case(i) for i in hd]
            con_doc = []
            if hd:
                box2 = html.xpath("//div[@id='consultees']/div[@class='list']/div[2]/div")
                for i in box2:
                    bd = i.xpath(".//descendant::div")
                    all = []
                    for b in bd:
                        tx = b.xpath(".//descendant::text()").get()
                        if not tx:
                            tx = ""
                        all.append(tx)
                    
                    if bd:
                        x = 0
                        e_rel = {}
                        for ii in all:
                            
                            hed = hd[x]
                            try:
                                e_rel[hed] = stripper(ii)
                            except:
                                print('Couldnt unpack')
                            x+=1
                        con_doc.append(e_rel)
                    each['consultees'] = con_doc

            #publicnotices
            box2  = html.xpath("//div[@id='publicnotices']/div[@class='list']")
            hd = box2.xpath(".//div[1]/div/text()").getall()
            hd = [camel_case(i) for i in hd]
            con_doc = []
            if hd:
                box2 = html.xpath("//div[@id='publicnotices']/div[@class='list']/div[2]/div")
                for i in box2:
                    bd = i.xpath(".//descendant::div")
                    all = []
                    for b in bd:
                        tx = b.xpath(".//descendant::text()").get()
                        if not tx:
                            tx = ""
                        all.append(tx)
                    
                    if bd:
                        x = 0
                        e_rel = {}
                        for ii in all:
                            
                            hed = hd[x]
                            try:
                                e_rel[hed] = stripper(ii)
                            except:
                                print('Couldnt unpack')
                            x+=1
                        con_doc.append(e_rel)
                    each['publicNotices'] = con_doc

            #documents
            box2  = html.xpath("//tr[@class='header']/following-sibling::tr")
            con_doc = []
            if box2:
                for i in box2:
                    try:
                        e_rel={}
                        l = stripper(i.xpath(".//td[1]/descendant::a/@href").get())
                        if l:

                            e_rel['documentLink'] = 'https://planning.redcar-cleveland.gov.uk'+ l
                            e_rel['documentType'] = stripper(i.xpath(".//td[1]/descendant::a/text()").get())
                            e_rel['size'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                            e_rel['date'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                                
                            con_doc.append(e_rel)
                    except:
                        pass
                each['documents'] = con_doc

            yield each

