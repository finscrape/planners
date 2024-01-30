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


class SouthderbyshireSpider(scrapy.Spider):
    name = "southderbyshire"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = 0
        self.total = []
        self.driver = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
        self.driver.maximize_window()

        # self.drivera = webdriver.Firefox(options=options,service=Service(GeckoDriverManager().install()))
        # self.drivera.maximize_window()
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    
    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")
    def parse(self, response):

        self.driver.get('https://planning.southderbyshire.gov.uk/')

        try:
            self.driver.find_element("xpath","//select[@id='Mainpage_FromDay']").click()
            self.driver.find_element("xpath","//select[@id='Mainpage_FromDay']/option[1]").click()
            
            self.driver.find_element("xpath","//select[@id='Mainpage_FromMonth']").click()
            self.driver.find_element("xpath","//select[@id='Mainpage_FromMonth']/option[1]").click()
            
            self.driver.find_element("xpath","//select[@id='Mainpage_FromYear']").click()
            self.driver.find_element("xpath","//select[@id='Mainpage_FromYear']/option[1]").click()



            self.driver.find_element("xpath","//select[@id='Mainpage_ToDay']").click()
            self.driver.find_element("xpath","//select[@id='Mainpage_ToDay']/option[1]").click()

            self.driver.find_element("xpath","//select[@id='Mainpage_ToMonth']").click()
            self.driver.find_element("xpath","//select[@id='Mainpage_FromMonth']/option[1]").click()
            
            self.driver.find_element("xpath","//select[@id='Mainpage_ToYear']").click()
            self.driver.find_element("xpath","//select[@id='Mainpage_ToYear']/option[26]").click()

            
            
            sleep(1)
            self.driver.find_element("xpath","//input[@id='Mainpage_cmdSearch']").click()
            
        except:
            pass
        

        
        num = 1
        while num <= 1915:
            cl = self.driver.current_url
            #get planning apllications link
            alinks = self.driver.find_elements("xpath","//tr[@style='color:White;background-color:#4E8539;font-weight:bold;']/following-sibling::tr/td[8]/input")
            st = 0
            for aa in alinks:
                print(f'{num}----page planning applications')
                print(f'{num}----page planning applications')
                print(f'{num}----page planning applications')
                print(f'{num}----page planning applications')

                try:
                    alinks = self.driver.find_elements("xpath","//tr[@style='color:White;background-color:#4E8539;font-weight:bold;']/following-sibling::tr/td[8]/input")
                
                    alinks[st].click()
                    sleep(2)
                    pagea = self.driver.page_source
                    htmla = Selector(text=pagea)

                    path = htmla.xpath("//table[@id='Mainpage_detailPlanning']/descendant::tr/td[@align='right']").getall()
                    if path:
                        each = {}
                        each['planningUrl'] = self.driver.current_url
                        table_hd = htmla.xpath("//table[@id='Mainpage_detailPlanning']/descendant::tr/td[@align='right']")
                        if table_hd:
                            for i in table_hd:
                                first = i.xpath(".//text()").get()
                                second = i.xpath(".//following-sibling::td/text()").getall()
                                if second:
                                    second = ''.join(second)
                                    second = stripper(second)
                                else:
                                    second = ""

                                try:
                                    fir = camel_case(first)

                                    each[fir] = second
                                except:
                                    pass
                    else:
                        each = {}
                        each['planningUrl'] = self.driver.current_url
                        table_hd = htmla.xpath("//span[@class='test-id__field-label']")
                        if table_hd:
                            for i in table_hd:
                                first = i.xpath(".//text()").get()
                                second = i.xpath(".//ancestor::div[1]/following-sibling::div/descendant::text()").getall()
                                if second:
                                    second = ''.join(second)
                                    second = stripper(second)
                                else:
                                    second = ""

                                try:
                                    fir = camel_case(first)

                                    each[fir] = second
                                except:
                                    pass
                        yield each
                            
                        
                

                    

                    self.listhref.append(htmla)
                    st+=1
                    self.driver.get(cl)
                except:
                    pass


            
            self.driver.find_element('xpath',"//tr[1][@style='color:White;background-color:#4E8539;font-size:11pt;']/descendant::tr/td/span/ancestor::td[1]/following-sibling::td[1]/a").click()
            
            
            
            num+=1

    def spider_closed(self, spider):
        self.driver.close()
        spider.logger.info("Spider closed: %s", spider.name)
            

            