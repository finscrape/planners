import scrapy
from planners.util import dates_str9
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


class IpswichSpider(scrapy.Spider):
    name = "ipswich"
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
        # dispatcher.connect(self.spider_closed,signals.spider_closed)

    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
        start = 0
        
        for d in dates_str9[0:-1]:

            start += 1
            fd = d
            ffd = fd.split("/")
            
            ffd = ffd[-1]
            ffd = int(ffd)
            if ffd < 1948:
                print('Too old to search from')
                continue

            nd = dates_str9[start]
            try:
                self.driver.get("https://ppc.ipswich.gov.uk/appnsearch.asp")
                sleep(3)
            except:
                try:
                    self.driver.get("https://ppc.ipswich.gov.uk/appnsearch.asp")
                    sleep(3)
                except:
                    continue

            try:
                #date picker
                fromDate = self.driver.find_element("xpath","//input[@name='txtValStartDate']")

                fromDate.clear()

                fromDate.send_keys(fd)

                fromto = self.driver.find_element("xpath","//input[@name='txtValEndDate']")
                fromto.clear()

                fromto.send_keys(nd)
            except:
                continue

            sleep(1)

            try:
                self.driver.find_element('xpath',"//input[@name='imgSubmit']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//input[@name='imgSubmit']").click()
                except:
                    pass

            
            sleep(3)
            try:
                pagex = self.driver.page_source
                html = Selector(text=pagex)
            except:
                continue
            links = html.xpath("//tr/td/a[1]/@href").getall()
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
                    searchPl = self.driver.find_element("xpath","(//a/img[@title='Next Page'])[1]")
                    self.driver.execute_script("arguments[0].scrollIntoView();", searchPl)
                    self.driver.execute_script("arguments[0].click();", searchPl)
                    
                    sleep(3)
                    page = self.driver.page_source
                    html = Selector(text=page)
                    links = html.xpath("//tr/td/a[1]/@href").getall()
                    
                    self.listhref.extend(links)
                    print(f'From {fd} to {nd}------getting the {x} pageeee')
                    print(f'From {fd} to {nd}------getting the {x} pageeee')
                    print(f'From {fd} to {nd}------getting the {x} pageeee')
                    
                    
                    
                except:
                    break
        
        self.drivera.get("https://ppc.ipswich.gov.uk/appnsearch.asp")
        sleep(3)

        try:
            #date picker
            fromDate = self.drivera.find_element("xpath","//input[@name='txtValStartDate']")

            fromDate.clear()

            fromDate.send_keys("01/02/2020")

            fromto = self.drivera.find_element("xpath","//input[@name='txtValEndDate']")
            fromto.clear()

            fromto.send_keys("10/02/2020")
        except:
            pass

        sleep(1)

        try:
            self.drivera.find_element('xpath',"//input[@name='imgSubmit']").click()
        except:
            try:
                self.drivera.find_element('xpath',"//input[@name='imgSubmit']").click()
            except:
                pass

        
        sleep(3)

        for i in self.listhref:
            
            abs_i = f'https://ppc.ipswich.gov.uk/{i}'
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
            box = html.xpath("//label")
            for i in box:
                table_hd = i.xpath(".//descendant::text()").get()
                table_hd = stripper(table_hd)
                second = i.xpath(".//ancestor::th[1]/following-sibling::td[1]/input/@value").getall()
                if not second:
                    second = i.xpath(".//ancestor::th[1]/following-sibling::td[1]/textarea/text()").getall()

                
                allsecond = ''.join(second)
                allsecond = stripper(allsecond)
                try:
                    fir = camel_case(table_hd)

                    each[fir] = allsecond
                except:
                    each[table_hd] = allsecond

            each['decisionNoteExplained'] = 'https://ppc.ipswich.gov.uk/xhelpdecn.asp'

            nt = html.xpath("//span[contains(@id,'doc_dec_View_decision_notice')]/a[1]/@href").get()
            if nt:
                each['viewDecisionNotice'] = 'https://ppc.ipswich.gov.uk/' + nt

            nt = html.xpath("//span[contains(@id,'doc_app_View_site_notice')]/a[1]/@href").get()
            if nt:
                each['viewSiteNotice'] = 'https://ppc.ipswich.gov.uk/' + nt

            nt = html.xpath("//span[contains(@id,'doc_sum_Summary_application')]/a[1]/@href").get()
            if nt:
                each['officerReport'] = 'https://ppc.ipswich.gov.uk/' + nt

            
            #documents
            id = html.xpath("//input[@id='txtAppNo']/@value").get()
            try:
                doclink = f'https://ppc.ipswich.gov.uk/xappndocs.asp?iAppID={id}'
                self.drivera.get(doclink)
                page = self.drivera.page_source
                html = Selector(text=page)
                sleep(1.5)

                rd = html.xpath("//table[@class='resulttable']/descendant::tr")
                if rd:
                    doc_doc = []
                    for i in rd[1:]:
                        try:
                            e_rel={}
                            e_rel['documentType'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                            e_rel['reference'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                            e_rel['description'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                            e_rel['dateReceived'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                            e_rel['sizeOfDoc'] = stripper(i.xpath(".//td[5]/descendant::text()").get())
                            l = stripper(i.xpath(".//td[6]/descendant::a/@href").get())
                            if l:
                                e_rel['fileLink'] = 'https://ppc.ipswich.gov.uk/' + l
                            
                            
                            doc_doc.append(e_rel)
                        except:
                            pass
                        
                    each['documents'] = doc_doc
            except:
                pass
            #consultees
            try:

                doclink = f'https://ppc.ipswich.gov.uk/xappncons.asp?iAppID={id}'
                self.drivera.get(doclink)
                page = self.drivera.page_source
                html = Selector(text=page)
                sleep(1.5)

                rd = html.xpath("//table[@class='resulttable']/descendant::tr")
                if rd:
                    doc_doc = []
                    for i in rd[1:]:
                        try:
                            e_rel={}
                            e_rel['consulteeCode'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                            e_rel['name'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                            e_rel['dateConsulted'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                            e_rel['dateReply'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                            e_rel['sizeOfDoc'] = stripper(i.xpath(".//td[5]/descendant::text()").get())
                            l = stripper(i.xpath(".//td[6]/descendant::a/@href").get())
                            
                            doc_doc.append(e_rel)
                        except:
                            pass
                        
                    each['consultees'] = doc_doc
            except:
                pass
            yield each

    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()

        spider.logger.info("Spider closed: %s", spider.name)
    