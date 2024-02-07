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




class WychavondistrictcouncilSpider(scrapy.Spider):
    name = 'wychavonDistrictCouncil'
    # allowed_domains = ['a.com']
    # start_urls = ['http://a.com/']

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = 0
        self.total = []
        self.driver = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
        self.driver.maximize_window()

        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def start_requests(self):
        yield scrapy.Request(url='https://www.ebay.com',callback=self.parse)
                

    def parse(self, response):
        start=0
        for d in dates_str5[0:-1]:
            start += 1
            fd = d
            nd = dates_str5[start]

            self.driver.get('https://plan.wychavon.gov.uk/Search/Advanced')
            #choose planning applications
            if fd == dates_str5[0]:
                try:
                    self.driver.find_element("xpath","//input[@id='SearchPlanning']").click()
                except:
                    try:
                        self.driver.find_element("xpath","//input[@id='SearchPlanning']").click()
                    except:
                        pass

            
            fromDate = self.driver.find_element("xpath","//input[@id='DateReceivedFrom']")

            fromDate.clear()

            fromDate.send_keys(fd)

            fromto = self.driver.find_element("xpath","//input[@id='DateReceivedTo']")
            fromto.clear()

            fromto.send_keys(nd)


            searchPl = self.driver.find_element('xpath',"//button[text()='Search']")
            searchPl.click()
            sleep(1)

            #get planning apllications link
            page = self.driver.page_source
            html = Selector(text=page)
            li = html.xpath("//a[contains(@href,'/Planning/Display')]/@href").getall()
            self.listhref.extend(li)
            last = html.xpath("//li[contains(a/text(),'Next')]/preceding-sibling::li")
            if last:
                lastt = last[-1]
                last_num = lastt.xpath(".//a/text()").get()
                print(f'{last_num}- planning applications')
                print(f'{last_num}- planning applications')
                print(f'{last_num}- planning applications')
                print(f'{last_num}- planning applications')
                num = 1
                while num < int(last_num):
                    try:
                        self.driver.find_element('xpath',"//li[contains(a/text(),'Next')]/a").click()
                        sleep(2)
                        page = self.driver.page_source
                        html = Selector(text=page)
                        li = html.xpath("//a[contains(@href,'/Planning/Display')]/@href").getall()
                        self.listhref.extend(li)
                        num+=1
                    except:
                        break
        for c in self.listhref:
                
            abs_i = f'https://plan.wychavon.gov.uk{c}'
            yield scrapy.Request(url=abs_i,callback=self.final,dont_filter=True)

    def final(self,response):     
        each = {}
        each['planningUrl'] = response.url
        table_hd = response.xpath("//div[@id='MainDetails']/descendant::table[1]/descendant::tr")
        for i in table_hd:
            first = i.xpath(".//td[1]/text()").get()
            if first in ['Summary','Important Dates','Further Information','Condition Details / Information Notes']:
                pass
            else:
                second = i.xpath(".//td[1]/following-sibling::td[1]/descendant::text()").getall()
                second = ''.join(second)
                second = stripper(second)
                fir = camel_case(first)

                each[fir] = second

        table_hd = response.xpath("//div[@id='MainDetails']/descendant::table[2]/descendant::tr")
        for i in table_hd:
            first = i.xpath(".//td[1]/text()").get()
            if first in ['Summary','Important Dates','Further Information','Condition Details / Information Notes']:
                pass
            else:
                second = i.xpath(".//td[1]/following-sibling::td[1]/descendant::text()").getall()
                second = ''.join(second)
                second = stripper(second)
                fir = camel_case(first)

                each[fir] = second

        table_hd = response.xpath("//div[@id='MainDetails']/descendant::table[3]/descendant::tr")
        for i in table_hd:
            first = i.xpath(".//td[1]/text()").get()
            if first in ['Summary','Important Dates','Further Information','Condition Details / Information Notes']:
                pass
            else:
                second = i.xpath(".//td[1]/following-sibling::td[1]/descendant::text()").getall()
                second = ''.join(second)
                second = stripper(second)
                fir = camel_case(first)

                each[fir] = second

        empty = []
        table_hd = response.xpath("//div[@id='MainDetails']/descendant::table[4]/descendant::tr")
        if table_hd:
            for i in table_hd[1:]:
                first = i.xpath(".//td/descendant::text()").get()
                empty.append(first)
            each['conditionDetailsInformationNotes'] = empty
                
        yield each
        self.total.append(each)
        

    def spider_closed(self, spider):
        self.driver.close()
        spider.logger.info("Spider closed: %s", spider.name)
        