import scrapy
from planners.util import dates_strz
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


class BournemouthSpider(scrapy.Spider):
    name = "bournemouth"
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
        #dispatcher.connect(self.spider_closed,signals.spider_closed)

    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
        start = 0
        
        for d in dates_strz[0:-1]:

            start += 1
            fd = d
            ffd = fd.split("/")
            
            ffd = ffd[-1]
            ffd = int(ffd)
            if ffd < 1980:
                print('Too old to search from')
                continue

            nd = dates_strz[start]
            
            self.driver.get("https://planning.bournemouth.gov.uk/disclaimer.aspx?returnURL=%2f")

            try:
                self.driver.find_element('xpath',"//input[@value='Accept']").click()
            except:
                pass
            
            sleep(1)
            
            try:
                #date picker
                fromDate = self.driver.find_element("xpath","//input[@id='ctl00_MainContent_txtDateReceivedFrom']")

                fromDate.clear()

                fromDate.send_keys(fd)

                fromto = self.driver.find_element("xpath","//input[@id='ctl00_MainContent_txtDateReceivedTo']")
                fromto.clear()

                fromto.send_keys(nd)
            except:
                continue

            sleep(1)


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

            links = html.xpath("//tr[contains(@class,'Row')]/td[2]/a/@href").getall()
            if not links:
                continue
            
            
            for i in links:
                abs_i  =f'https://planning.bournemouth.gov.uk/{i}'
                self.listhref.append(abs_i)

            x = 1
            while True:
                try:
                    nextPl = self.driver.find_element('xpath',"//input[@title='Next Page']")
                    self.driver.execute_script("arguments[0].scrollIntoView();", nextPl)
                    self.driver.execute_script("arguments[0].click();", nextPl)
                    
                    try:
                        self.driver.find_element('xpath',"//input[@value='Accept']").click()
                    except:
                        pass
                    sleep(2)
                    x += 1
                    print(f'{x} page scraped')
                    print(f'{x} page scraped')
                    print(f'{x} page scraped')
                    print(f'{x} page scraped')
                    page = self.driver.page_source
                    html = Selector(text=page)

                    links = html.xpath("//tr[contains(@class,'Row')]/td[2]/a/@href").getall()
                    
                    for i in links:
                        abs_i  =f'https://planning.bournemouth.gov.uk/{i}'
                        self.listhref.append(abs_i)
                    
                    check = html.xpath("//input[@title='Next Page' and @onclick ='return false;']")
                    if check:
                        break
                

                except:
                    try:
                        nextPl = self.driver.find_element('xpath',"//input[@title='Next Page']")
                        self.driver.execute_script("arguments[0].scrollIntoView();", nextPl)
                        self.driver.execute_script("arguments[0].click();", nextPl)
                        try:
                            self.driver.find_element('xpath',"//input[@value='Accept']").click()
                        except:
                            pass
                        
                         
                        sleep(3)
                        x += 1
                        print(f'{x} page scraped')
                        print(f'{x} page scraped')
                        print(f'{x} page scraped')
                        print(f'{x} page scraped')
                        page = self.driver.page_source
                        html = Selector(text=page)
                        
                        

                        links = html.xpath("//tr[contains(@class,'Row')]/td[2]/a/@href").getall()
                        
                        for i in links:
                            abs_i  =f'https://planning.bournemouth.gov.uk/{i}'
                            self.listhref.append(abs_i)
                            
                        check = html.xpath("//input[@title='Next Page' and @onclick ='return false;']")
                        if check:
                            break
                    except:
                        break
                    
        self.drivera.get("https://planning.bournemouth.gov.uk/disclaimer.aspx?returnURL=%2f")

        try:
            self.drivera.find_element('xpath',"//input[@value='Accept']").click()
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
        sleep(10)

        for ai in self.listhref:
            try:
                self.drivera.get(ai)
                sleep(2)
            except:
                try:
                    self.drivera.get(ai)
                    sleep(2)
                except:
                    continue
            
            
            try:
                self.drivera.find_element('xpath',"//input[@value='Accept']").click()
            except:
                pass
            
            sleep(1)

            page = self.drivera.page_source
            html = Selector(text=page)

            
            each = {}
            each['planningUrl'] = ai

            box = html.xpath("//label")
            for i in box:
                table_hd = i.xpath(".//text()").get()
                if table_hd:
                    table_hd = stripper(table_hd)
                    second = i.xpath(".//ancestor::td[1]/following-sibling::td[1]/input/@value").getall()
                    if not second:
                        second = i.xpath(".//ancestor::td[1]/following-sibling::td[1]/textarea/text()").getall()
                        if not second:
                            second = i.xpath(".//ancestor::td[1]/following-sibling::td[1]/select/option/@value").getall()

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
            
            box2 = html.xpath("//td[contains(@class,'track')]")
            for i in box2:
                table_hd = i.xpath(".//text()[1]").get()
                if table_hd:
                    table_hd = stripper(table_hd)
                    second = i.xpath(".//text()[2]").getall()
                    
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

            try:
                self.drivera.find_element("xpath","//span[text()='Associated Documents']").click()
                sleep(2)
            except:
                html = None
                
            try:
                self.drivera.find_element('xpath',"//input[@value='Accept']").click()
            except:
                pass

            page = self.drivera.page_source
            html = Selector(text=page)

            #documents
            if html:
                box2  = html.xpath("//table[@id='ctl00_MainContent_gridDocuments']/descendant::tr")
                con_doc = []
                if box2:
                
                    for i in box2[1:]:
                        try:
                            e_rel={}
                            
                            e_rel['fileName'] = stripper(i.xpath(".//td[1]/descendant::a/text()").get())
                            e_rel['fileDescription'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                            e_rel['date'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                                
                            con_doc.append(e_rel)
                        except:
                            pass
                    each['allDocuments'] = con_doc


            yield each

    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()

        spider.logger.info("Spider closed: %s", spider.name)
    