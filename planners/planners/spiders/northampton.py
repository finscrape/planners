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



class NorthamptonSpider(scrapy.Spider):
    name = "northampton"
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
        yield scrapy.Request(url='https://maps.rochford.gov.uk/DevelopmentControl.aspx?RequestType=ParseTemplate&template=DevelopmentControlAdvancedSearch.tmplt')

    def parse(self, response):
        self.driver.get("https://wnc.planning-register.co.uk/Search/Advanced")

        try:
            self.driver.find_element('xpath',"//input[@value='Agree']").click()
        except:
            sleep(45)
            try:
                self.driver.find_element('xpath',"//input[@value='Agree']").click()
            except:
                print('error with agree mutton')
        

        try:
            self.driver.find_element('xpath',"//input[@id='SearchPlanning']").click()
        except:
            sleep(45)
            try:
                self.driver.find_element('xpath',"//input[@id='SearchPlanning']").click()
            except:
                print('error with plannin mutton')
        

        try:
            self.driver.find_element('xpath',"//button[@id='submitBtn']").click()
            
        except:
            sleep(60)
            self.driver.find_element('xpath',"//button[@id='submitBtn']").click()
        

        sleep(45)
        pagex = self.driver.page_source
        html = Selector(text=pagex)
        links = html.xpath("//span[text()='Reference No.']/following-sibling::strong/a/@href").getall()
        self.listhref.extend(links)
        print(self.listhref)

        x = 0
        while True:
            x += 1
            if x > 24200:
                break
            try:
                k =self.driver.find_element("xpath","//a[text()='Next']")
                self.driver.execute_script("arguments[0].scrollIntoView();", k)
                self.driver.execute_script("arguments[0].click();", k)
                sleep(5)
                page = self.driver.page_source
                html = Selector(text=page)
                links = html.xpath("//span[text()='Reference No.']/following-sibling::strong/a/@href").getall()
                self.listhref.extend(links)

                
            except:
                break
        

        for i in self.listhref:
            abs_i = f'https://wnc.planning-register.co.uk{i}'
            yield scrapy.Request(url='https://www.ebay.com',meta={'u':abs_i},callback=self.parsedetails,dont_filter=True)

    def parsedetails(self,response):
        u =response.meta['u']
        self.drivera.get(u)

        try:
            self.drivera.find_element('xpath',"//input[@value='Agree']").click()
        except:
            pass
        
        try:
            self.drivera.find_element('xpath',"//input[@value='Agree']").click()
        except:
            pass
       
        
        cur = self.drivera.current_url
        self.drivera.get(cur)
        
        page = self.drivera.page_source
        html = Selector(text=page)

        box0 = html.xpath("//div[@id='Main Details']/descendant::tr/td")
        box1 = html.xpath("//div[@id='Applicant/ Agents']/descendant::tr/td")

        box2 = html.xpath("//div[@id='Addresses']/descendant::tr[1]/th/text()").get()
        box2_text = html.xpath("//div[@id='Addresses']/descendant::tr[2]/td/text()").get()
        each = {}
        each[box2] = box2_text

        for i in box0:
            first = i.xpath(".//text()").get()
            if first:
                second = i.xpath(".//div/descendant::text()").getall()
                second = ''.join(second)
                
                second = second.replace('\r','').replace('\n','').replace('\t','').replace(":","").strip()
                

                try:
                    fir = camel_case(first)

                    each[fir] = second
                except:
                    each[first] = second

        for i in box1:
            first = i.xpath(".//text()").get()
            if first:
                second = i.xpath(".//div/descendant::text()").getall()
                second = ''.join(second)
                
                second = second.replace('\r','').replace('\n','').replace('\t','').replace(":","").strip()
                

                try:
                    fir = camel_case(first)

                    each[fir] = second
                except:
                    each[first] = second



        
        yield each
        self.total.append(each)
        