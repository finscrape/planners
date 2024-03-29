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




class CamdenSpider(scrapy.Spider):
    name = "camden"
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
            nd = dates_strx[start]

            self.driver.get("https://planningrecords.camden.gov.uk/NECSWS/PlanningExplorer/GeneralSearch.aspx")
            sleep(3)

            try:
                self.driver.find_element('xpath',"//input[@id='rbRange']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//input[@id='rbRange']").click()
                except:
                    pass
            try:
                #date picker
                fromDate = self.driver.find_element("xpath","//input[@id='dateStart']")

                fromDate.clear()

                fromDate.send_keys(fd)

                fromto = self.driver.find_element("xpath","//input[@id='dateEnd']")
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
            links = html.xpath("//td[@title='View Application Details']/a/@href").getall()
            self.listhref.extend(links)
            print('Date search')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')


            x = 0
            while True:
                x += 1
              
                try:
                    searchPl = self.driver.find_element("xpath","//img[contains(@title,'Go to next')]")
                    self.driver.execute_script("arguments[0].scrollIntoView();", searchPl)
                    self.driver.execute_script("arguments[0].click();", searchPl)
                    
                    sleep(1)
                    page = self.driver.page_source
                    html = Selector(text=page)
                    links = html.xpath("//td[@title='View Application Details']/a/@href").getall()
                    self.listhref.extend(links)
                    print(f'From {fd} to {nd}------getting the {x} pageeee')
                    print(f'From {fd} to {nd}------getting the {x} pageeee')
                    print(f'From {fd} to {nd}------getting the {x} pageeee')
                    
                except:
                    break
        
                #opening drivera page...stabilize page
        
        
        self.drivera.get("https://planningrecords.camden.gov.uk/NECSWS/PlanningExplorer/GeneralSearch.aspx")
        sleep(2)

        try:
            self.drivera.find_element('xpath',"//input[@id='rbRange']").click()
        except:
            try:
                self.drivera.find_element('xpath',"//input[@id='rbRange']").click()
            except:
                pass
        #date picker
        fromDate = self.drivera.find_element("xpath","//input[@id='dateStart']")

        fromDate.clear()

        fromDate.send_keys("01/01/2020")

        fromto = self.drivera.find_element("xpath","//input[@id='dateEnd']")
        fromto.clear()

        fromto.send_keys("10/01/2020")

        try:
            self.drivera.find_element('xpath',"//input[@value='Search']").click()
        except:
            try:
                self.drivera.find_element('xpath',"//input[@value='Search']").click()
            except:
                pass
        sleep(2)
        for i in self.listhref:
            i = stripper(i)
            ispl = i.split(" ")
            newi = '%20'.join(ispl)
        
            abs_i = f'https://planningrecords.camden.gov.uk/NECSWS/PlanningExplorer/Generic/{newi}'
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
            box = html.xpath("//h1[text()='Application Details']/following-sibling::ul/li/descendant::span")
            for i in box:
                table_hd = i.xpath(".//text()").get()
                table_hd = stripper(table_hd)
                second = i.xpath(".//following-sibling::text()").getall()
                allsecond = ''.join(second)
                allsecond = stripper(allsecond)
                try:
                    fir = camel_case(table_hd)

                    each[fir] = allsecond
                except:
                    each[table_hd] = allsecond

            
            olinks = html.xpath("(//a[contains(@title,'Neighbours')]/@href  | //a[contains(@title,'Consultee')]/@href  | //a[contains(@title,'Constraint')]/@href  |   //a[contains(@title,'Dates page')]/@href | //a[contains(@title,'Checks')]/@href | //a[contains(@title,'Meeting')]/@href)").getall()
            doclinks = html.xpath("(//a[contains(@title,'Document')]/@href)[1]").get()
            
            for a in olinks:
                if 'http' not in a:
                    abs_a = f'https://planningrecords.camden.gov.uk/NECSWS/PlanningExplorer/Generic/{a}'
                    
                    self.drivera.get(abs_a)
                    page = self.drivera.page_source
                    html = Selector(text=page)

                    box = html.xpath("//ul/li/div/span")
                    if box:
                        for i in box:
                            table_hd = i.xpath(".//text()").get()
                            table_hd = stripper(table_hd)
                            second = i.xpath(".//following-sibling::text()").getall()
                            allsecond = ''.join(second)
                            allsecond = stripper(allsecond)
                            try:
                                fir = camel_case(table_hd)

                                each[fir] = allsecond
                            except:
                                each[table_hd] = allsecond
                    else:
                        check = html.xpath("//h1[contains(text(),'Neighbour details')]")
                        if check:
                            each['neighbourLocation'] = html.xpath("//span[text() = 'Location']/following-sibling::text()").get()
                            each['neighbourAddresses'] = html.xpath("//h1[text() = 'Addresses']/following-sibling::ul/li/div/descendant::text()").getall()
                    
            if doclinks:
                doc_doc =[]
                self.drivera.get(doclinks)
                page = self.drivera.page_source
                html = Selector(text=page)
                sleep(1.5)

                rd = html.xpath("//table[@id='recordtable']/descendant::tr")
            
                for i in rd[1:]:
                    e_rel={}
                    e_rel['dateCreated'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                    e_rel['title'] = stripper(i.xpath(".//td[2]/descendant::a/text()").get())
                    l = stripper(i.xpath(".//td[2]/descendant::a/@href").get())
                    if l:
                        e_rel['fileLink'] = 'https://camdocs.camden.gov.uk/' + l
                    
                    e_rel['documentType'] = stripper(i.xpath(".//td[3]/descendant::a/text()").get())
                    doc_doc.append(e_rel)
                
                each['documents'] = doc_doc


            yield each
            self.total.append(each)
            
    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()

        spider.logger.info("Spider closed: %s", spider.name)
    