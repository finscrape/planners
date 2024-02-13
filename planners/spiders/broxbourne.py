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


class BroxbourneSpider(scrapy.Spider):
    name = "broxbourne"
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
        
        
        for d in dates_strx[0:-1]:

            start += 1
            fd = d
            ffd = fd.split("/")
            
            ffd = ffd[-1]
            ffd = int(ffd)
            if ffd < 1990:
                print('Too old to search from')
                continue
            
            nd = dates_strx[start]
            try:
                self.driver.get("https://www.bookstoscrape.com")
            except:
                pass
            
            try:
        
                self.driver.get("https://planning.broxbourne.gov.uk/LPAssure/ES/Presentation/Planning/OnlinePlanning/OnlinePlanningSearch#")
                sleep(3)
            except:
                try:
            
                    self.driver.get("https://planning.broxbourne.gov.uk/LPAssure/ES/Presentation/Planning/OnlinePlanning/OnlinePlanningSearch#")
                    sleep(3)
                except:
                    continue
                
            try:
                self.driver.find_element("xpath","//a[@onclick='AcceptCookies();']").click()
            except:
                try:
                    self.driver.find_element("xpath","//a[@onclick='AcceptCookies();']").click()
                except:
                    pass
            sleep(2)
            
            try:
                self.driver.find_element("xpath","//a[text()='Advanced search']").click()
            except:
                try:
                    self.driver.find_element("xpath","//a[text()='Advanced search']").click()
                except:
                    pass
            sleep(2)

            
            
            try:
                self.driver.find_element("xpath","//input[@id='AdvanceSearch_ReceivedBetween']").click()
            except:
                try:
                    self.driver.find_element("xpath","//input[@id='AdvanceSearch_ReceivedBetween']").click()
                except:
                    pass
            sleep(1)
            

            try:
                #date picker
                fromDate = self.driver.find_element("xpath","//input[@id='AdvanceSearch_ReceivedFromDate']")

                fromDate.clear()

                fromDate.send_keys(fd)

                fromto = self.driver.find_element("xpath","//input[@id='AdvanceSearch_ReceivedToDate']")
                fromto.clear()

                fromto.send_keys(nd)
            except:
                pass

            

            sleep(1)
            try:
                self.driver.find_element('xpath',"//a[text()='Search']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//a[text()='Search']").click()
                except:
                    pass
            sleep(5)
            
            

            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//a[@onclick='SearchRecord(this);']/@data-redirect-url").getall()
            if not links:
                continue
            
            self.listhref.extend(links)
            
            
            x = 0
            while True:
                x += 1
                
                try:
                    searchPl = self.driver.find_element("xpath","//a[@class='btn-primary active']/following-sibling::a[1]")
                    self.driver.execute_script("arguments[0].scrollIntoView();", searchPl)
                    self.driver.execute_script("arguments[0].click();", searchPl)
                    
                    sleep(1.5)

                    pagex = self.driver.page_source
                    html = Selector(text=pagex)
                    links = html.xpath("//a[@onclick='SearchRecord(this);']/@data-redirect-url").getall()
                    if not links:
                        continue
                    
                    self.listhref.extend(links)
                    
                    print(f'From  -----getting the {x} pageeee')
                    print(f'From ------getting the {x} pageeee')
                    print(f'From ------getting the {x} pageeee')

                    
                except:
                    break


        self.drivera.get("https://planning.broxbourne.gov.uk/LPAssure/ES/Presentation/Planning/OnlinePlanning/OnlinePlanningSearch#")
        sleep(3)
        try:
            self.drivera.find_element("xpath","//a[@onclick='AcceptCookies();']").click()
        except:
            try:
                self.drivera.find_element("xpath","//a[@onclick='AcceptCookies();']").click()
            except:
                pass
        sleep(2)

        

        for i in self.listhref:
            ai = f'https://planning.broxbourne.gov.uk{i}'
            
            try:
                self.driver.get("https://www.bookstoscrape.com")
            except:
                pass
            
            try:
                self.drivera.get(ai)
            except:
                try:
                    self.drivera.get(ai)
                except:
                    continue
                

            sleep(3)
            try:
                page = self.drivera.page_source
                html = Selector(text=page)
            except:
                sleep(10)
                continue
                
            
            each = {}
            each['planningUrl'] = ai
            each['applicationId'] = html.xpath("//span[@id='spnApplicationId']/text()").get()
            if not each['applicationId']:
                continue
            
            each['applicationDisplayAddress'] = html.xpath("//label[@id='applicationDisplayAddress']/text()").get()

            box = html.xpath("//td[@class='width-30']")
            for i in box:
                table_hd = i.xpath(".//descendant::text()").get()
                if table_hd:
                    table_hd = stripper(table_hd)
                    second = i.xpath(".//following-sibling::td[1]/descendant::text()").getall()
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
                self.drivera.find_element("xpath","//li[@id='RelatedPlanningApplications_tab']/a").click()
                sleep(2)
            except:
                yield each
                continue

            page = self.drivera.page_source
            html = Selector(text=page)
            #related docs
            box2 = html.xpath("//div[@id='divRelatedPlanningApplications']/div[@class='row btspace']/preceding-sibling::div[1]")
            if box2:
                con_doc = []
                for i in box2:
                    e_rel = {}
                    title_n = i.xpath(".//a/span/text()").get()
                    title_l = i.xpath(".//a/@href").get()
                    if title_l:
                        title_n = title_n.replace('Application No:',"")
                        e_rel['applicationNo'] = title_n
                        e_rel["applicationLink"] = 'https://planning.broxbourne.gov.uk' + title_l

                        box3 = box2.xpath(".//following-sibling::div[1]")

                        e_rel['applicationType'] = stripper(box3.xpath(".//descendant::label[1]/following-sibling::text()").get())
                        e_rel['registered'] = stripper(box3.xpath(".//descendant::label[2]/following-sibling::text()").get())
                        e_rel['status'] = stripper(box3.xpath(".//descendant::label[3]/following-sibling::text()").get())
                    con_doc.append(e_rel)

                each['relatingPlanningApplications'] = con_doc

            
            try:
                self.drivera.find_element("xpath","//li[@id='Documents_tab']/a").click()
                
                sleep(2)
            except:
                yield each
                continue

            page = self.drivera.page_source
            html = Selector(text=page)
            #documents
            box2 = html.xpath("//form[@id='frmDocumentsMain']/descendant::div[@class='row btspace']")
            con_doc = []
            if box2:
                for i in box2[1:]:
                    try:
                        e_rel={}
                        l = stripper(i.xpath(".//div[2]/a/@href").get())
                        if l:

                            e_rel['documentLink'] = 'https://planning.broxbourne.gov.uk'+l
                            e_rel['documentDate'] = stripper(i.xpath(".//div[1]/descendant::text()").get())
                            e_rel['documentName'] = stripper(i.xpath(".//div[2]/a/u/text()").get())
                            e_rel['documentType'] = stripper(i.xpath(".//div[3]/descendant::text()").get())
                                
                            con_doc.append(e_rel)
                    except:
                        pass
                each['allDocuments'] = con_doc


            yield each

    def spider_closed(self, spider):
        try:
            self.driver.quit()
            self.drivera.quit()
        except:
            pass
        spider.logger.info("Spider closed: %s", spider.name)
      
