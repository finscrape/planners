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


class CumberlandcouncilSpider(scrapy.Spider):
    name = "cumberlandcouncil"
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

            self.driver.get("https://cumberlandcouncil.my.site.com/pr3/s/register-view?c__r=Arcus_BE_Public_Register")
        
            sleep(3)
            try:
                self.driver.find_element('xpath',"//button[text()='Advanced search']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//button[text()='Advanced search']").click()
                except:
                    pass


            
            

            sleep(3)

            try:
                self.driver.find_element('xpath',"//button[@id='combobox-button-15']").click()
                self.driver.find_element('xpath',"//span[@title='Planning Applications']").click()
                
            except:
                try:
                    self.driver.find_element('xpath',"//button[@id='combobox-button-15']").click()
                    self.driver.find_element('xpath',"//span[@title='Planning Applications']").click()

                
                except:
                    pass
            sleep(3)
                       
            #date picker
            fromDate = self.driver.find_element("xpath","//label[text()='Valid date from']/following-sibling::div/input")

            fromDate.clear()

            fromDate.send_keys(fd)

            fromto = self.driver.find_element("xpath","//label[text()='Valid date to']/following-sibling::div/input")
            fromto.clear()

            fromto.send_keys(nd)

            try:
                self.driver.find_element('xpath',"//button[text()='Search']").click()
            except:
                try:
                    self.driver.find_element('xpath',"//button[text()='Search']").click()
                except:
                    pass
            
            sleep(3)

            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//lightning-formatted-url/a/@href").getall()
            self.listhref.extend(links)

            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
            
            x = 0
            while True:
                x += 1
              
                try:
                    searchPl = self.driver.find_element("xpath","//a[contains(text(),'Next')]")
                    self.driver.execute_script("arguments[0].scrollIntoView();", searchPl)
                    self.driver.execute_script("arguments[0].click();", searchPl)
                    
                    sleep(2)
                    page = self.driver.page_source
                    html = Selector(text=page)
                    links = html.xpath("//lightning-formatted-url/a/@href").getall()
                    self.listhref.extend(links)
                    print(f'From {fd} to {nd}------getting the {x} pageeee')
                    print(f'From {fd} to {nd}------getting the {x} pageeee')
                    print(f'From {fd} to {nd}------getting the {x} pageeee')

                    
                except:
                    break

        done_url = []    
        for i in self.listhref[0:10]:
            
            abs_i = f'https://cumberlandcouncil.my.site.com{i}&tabset-dfed1=3'
            if abs_i not in done_url:
                done_url.append(abs_i)
                self.drivera.get(abs_i)
                sleep(2)

                pagex = self.drivera.page_source
                htmla = Selector(text=pagex)
                
                each = {}
                each['planningUrl'] = self.drivera.current_url
                each['planningApplication'] = htmla.xpath("//h1[@class='pr-heading']/text()").get()

                table_hd = htmla.xpath("//dt[@class='pr-summary-list__key']")
                for i in table_hd:

                    first = i.xpath(".//descendant::text()").get()
                    if first and first != "  ":
                        second = i.xpath(".//following-sibling::dd[1]/descendant::text()").getall()
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
                    nei_doc = []
                    rd = htmla.xpath("(//table[@class='pr-table'])/descendant::tr[@class='pr-table__row']")
                    check = rd.xpath(".//th[1]/text()").get()
                    if check == "Date":
                        for i in rd[1:]:
                            e_rel={}
                            e_rel['date'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                            e_rel['description'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                            e_rel['download'] = stripper(i.xpath(".//td[3]/descendant::a/@href").get())
                            nei_doc.append(e_rel)

                    con_doc = []
                    rd = htmla.xpath("(//table[@class='pr-table'])[1]/descendant::tr[@class='pr-table__row']")
                    check = rd.xpath(".//th[1]/text()").get()
                    if check == "Role":
                    
                        for i in rd[1:]:
                            e_rel={}
                            e_rel['role'] = stripper(i.xpath(".//td[1]/descendant::text()").get())
                            e_rel['address'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                            con_doc.append(e_rel)
                        
                    each['documents'] = nei_doc
                    each['consultation'] = con_doc
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
            
