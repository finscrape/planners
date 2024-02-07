import scrapy
from planners.util import dates_str
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


class FarehamSpider(scrapy.Spider):
    name = "fareham"
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
        start=0
        for d in dates_str[0:-1]:
            start += 1
            fd = d
            nd = dates_str[start]

            self.driver.get("https://www.fareham.gov.uk/casetrackerplanning/")
            try:
                self.driver.find_element('xpath',"//a[@id='lnkAllowCookies']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//a[@id='lnkAllowCookies']").click()
                except:
                    pass

            sleep(2)
            try:
                self.driver.find_element('xpath',"//a[@title='Advanced search']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//a[@title='Advanced search']").click()
                except:
                    pass

            sleep(3)
            #date picker
            fromDate = self.driver.find_element("xpath","//input[@id='uxStartDateDecisionTextBox']")

            fromDate.clear()

            fromDate.send_keys(fd)

            fromto = self.driver.find_element("xpath","//input[@id='uxStopDateDecisionTextBox']")
            fromto.clear()

            fromto.send_keys(nd)

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
            links = html.xpath("//div[@class='searchResultsCell']/a/@href").getall()
            self.listhref.extend(links)

            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
        
        done_url = []
        for i in self.listhref:
            abs_i = f'https://www.fareham.gov.uk/casetrackerplanning/{i}'
            if abs_i not in done_url:
                done_url.append(abs_i)
                self.drivera.get(abs_i)

                
                sleep(1)
                page = self.drivera.page_source
                htmla = Selector(text=page)
                

                each = {}
                each['planningUrl'] = self.drivera.current_url
                table_hd = htmla.xpath("//div[@class='coreDetailsFieldCells']")
                for i in table_hd:

                    first = i.xpath(".//descendant::text()").get()
                    if first and first != "  ":
                        first = stripper(first)
                        second = i.xpath(".//following-sibling::div[1]/descendant::text()").getall()
                        if second:
                            second = ''.join(second)
                            second = stripper(second)
                        else:
                            second = ""
                        try:
                            fir = camel_case(first)

                            each[fir] = second
                        except:
                            each[first] = second

                table_sd = htmla.xpath("//div[@class='detailsCells detailsFieldNames']")
                for i in table_sd:

                    first = i.xpath(".//descendant::text()").get()
                    if first and first != "  ":
                        first = stripper(first)
                        second = i.xpath(".//following-sibling::div[1]/descendant::text()").getall()
                        if second:
                            second = ''.join(second)
                            second = stripper(second)
                        else:
                            second = ""
                        try:
                            fir = camel_case(first)

                            each[fir] = second
                        except:
                            each[first] = second

                if each:
                    try:
                        self.drivera.find_element('xpath',"//a[@id='lnkAllowCookies']").click()
                    except:
                        try:
                            self.drivera.find_element('xpath',"//a[@id='lnkAllowCookies']").click()
                        except:
                            pass

                    try:
                        self.drivera.find_element('xpath',"//input[@id='BodyPlaceHolder_uxChangeView_Documents']").click()
                    except:
                        try:
                            self.drivera.find_element('xpath',"//input[@id='BodyPlaceHolder_uxChangeView_Documents']").click()
                        except:
                            pass
                    sleep(1)
                    pagea = self.drivera.page_source
                    htmla = Selector(text=pagea)
                

                    nei_doc = []
                    rd = htmla.xpath("//div[@class='docGridTable']/div[@class='docGridRow']")
                    for i in rd[1:]:
                        e_rel={}
                        e_rel['datePublished'] = stripper(i.xpath(".//div[1]/descendant::text()").get())
                        e_rel['documentType'] = stripper(i.xpath(".//div[2]/descendant::text()").get())
                        e_rel['description'] = stripper(i.xpath(".//div[3]/descendant::text()").get())
                        e_rel['viewDocument'] = "https://www.fareham.gov.uk/casetrackerplanning" + stripper(i.xpath(".//div[4]/descendant::a/@href").get())
                        nei_doc.append(e_rel)
                    
                    each['Documents'] = nei_doc
                    self.plan +=1
                    print(f'{self.plan} planning application')
                    print(f'{self.plan} planning application')
                    print(f'{self.plan} planning application')
                    print(f'{self.plan} planning application')
                    yield each
                    self.total.append(each)



    def spider_closed(self, spider):
        self.driver.close()
        self.drivera.close()
        spider.logger.info("Spider closed: %s", spider.name)
                        

            