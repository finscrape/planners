import scrapy
from planners.util import dates_str6
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

class CarmarthenshireSpider(scrapy.Spider):
    name = "carmarthenshire"
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
        
        
        for d in dates_str6[0:-1]:

            start += 1
            fd = d
            nd = dates_str6[start]

            self.driver.get("https://carmarthenshire.my.site.com/en/s/?tabset-a3431=3")
            sleep(3)

            try:
                #date picker
                fromDate = self.driver.find_element("xpath","(//div[@class='form-element uiInput uiInputDate uiInput--default uiInput--input uiInput--datetime'])[1]/input")

                fromDate.clear()

                fromDate.send_keys(fd)

                fromto = self.driver.find_element("xpath","(//div[@class='form-element uiInput uiInputDate uiInput--default uiInput--input uiInput--datetime'])[2]/input")
                fromto.clear()

                fromto.send_keys(nd)
            except:
                continue

            sleep(1)

            try:
                self.driver.find_element('xpath',"(//button)[2]").click()
            except:
                try:
                    self.driver.find_element('xpath',"(//button)[2]").click()
                except:
                    pass
            sleep(4)
            
            

            pagex = self.driver.page_source
            html = Selector(text=pagex)
            links = html.xpath("//a[contains(@href,'en/s/planning-application')]/@href").getall()
            if not links:
                continue
            self.listhref.extend(links)
            print('Date search')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')
            print(f'From {fd} to {nd}')

        for i in self.listhref:
            ai = f'https://carmarthenshire.my.site.com{i}'
            
            self.drivera.get(ai)

            sleep(3)
            page = self.drivera.page_source
            html = Selector(text=page)

            
            each = {}
            each['planningUrl'] = ai

            box = html.xpath("//div[@class='test-id__field-label-container slds-form-element__label']")
            for i in box:
                table_hd = i.xpath(".//span/descendant::text()").get()
                if table_hd:
                    table_hd = stripper(table_hd)
                    second = i.xpath(".//following-sibling::div[@class='slds-form-element__control slds-grid itemBody']/descendant::text()").getall()
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

            
            self.drivera.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            url_spl = ai.split("/")
            url_la = url_spl[-1]
            sleep(1)
            app = html.xpath("//span[@title='Appeals']/ancestor::a[1]/@href").get()
            if app:
                each['appeals']= f'https://carmarthenshire.my.site.com/en/s/appeal/related/{url_la}/arcusbuiltenv__AppealsPapp__r'

            dual = html.xpath("//span[@title='Planning Applications (Dual Application)']/ancestor::a[1]/@href").get()
            if dual:
                each['planningApplicationsDualApplication']= f'https://carmarthenshire.my.site.com/en/s/planning-application/related/{url_la}/Planning_Applications__r'

            chd = html.xpath("//span[@title='Child Applications']/ancestor::a[1]/@href").get()
            if chd:
                each['childApplications']= f'https://carmarthenshire.my.site.com/en/s/planning-application/related/{url_la}/arcusbuiltenv__Planning_Applications__r'

            try:
                url_spl = ai.split("/")
                url_la = url_spl[-1]
                r_url  = f'https://carmarthenshire.my.site.com/en/s/planning-application/related/{url_la}/arcusbuiltenv__Related_Parties__r'
                self.drivera.get(r_url)
                sleep(2)

                page = self.drivera.page_source
                html = Selector(text=page)
                #related parties
                box2 = html.xpath("//table/descendant::tr")
                con_doc = []
                if box2:
                    for i in box2[1:]:
                        try:
                            e_rel={}
                            e_rel['name'] = stripper(i.xpath(".//th[1]/descendant::text()").get())
                            e_rel['role'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                            e_rel['address'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                            con_doc.append(e_rel)
                        except:
                            pass
                    each['relatedParties'] = con_doc
            except:
                print('failure')
                print('failure')
                print('failure')

            
            try:
                url_spl = ai.split("/")
                url_la = url_spl[-1]
                r_url  = f'https://carmarthenshire.my.site.com/en/s/planning-application/related/{url_la}/arcusbuiltenv__Planning_Applications__r'
                self.drivera.get(r_url)
                sleep(2)

                page = self.drivera.page_source
                html = Selector(text=page)
                #related parties
                box2 = html.xpath("//table/descendant::tr")
                con_doc = []
                if box2:
                    for i in box2[1:]:
                        try:
                            e_rel={}
                            e_rel['planningApplication'] = stripper(i.xpath(".//th[1]/descendant::text()").get())
                            e_rel['status'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                            e_rel['detailedStatus'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                            e_rel['validDate'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                            e_rel['applicationType'] = stripper(i.xpath(".//td[5]/descendant::text()").get())
                            e_rel['proposal'] = stripper(i.xpath(".//td[6]/descendant::text()").get())
                            con_doc.append(e_rel)
                        except:
                            pass
                    each['allChildApplications'] = con_doc
            except:
                print('failure')
                print('failure')
                print('failure')

            try:
                url_spl = ai.split("/")
                url_la = url_spl[-1]
                r_url  = f'https://carmarthenshire.my.site.com/en/s/planning-application/related/{url_la}/Planning_Applications__r'
                self.drivera.get(r_url)
                sleep(2)

                page = self.drivera.page_source
                html = Selector(text=page)
                #related parties
                box2 = html.xpath("//table/descendant::tr")
                con_doc = []
                if box2:
                    for i in box2[1:]:
                        try:
                            e_rel={}
                            e_rel['planningApplicationName'] = stripper(i.xpath(".//th[1]/descendant::text()").get())
                            con_doc.append(e_rel)
                        except:
                            pass
                    each['allPlanningApplicationsDualApplication'] = con_doc
            except:
                print('failure')
                print('failure')
                print('failure')


            try:
                url_spl = ai.split("/")
                url_la = url_spl[-1]
                r_url  = f'https://carmarthenshire.my.site.com/en/s/appeal/related/{url_la}/arcusbuiltenv__AppealsPapp__r'
                self.drivera.get(r_url)
                sleep(2)

                page = self.drivera.page_source
                html = Selector(text=page)
                #related parties
                box2 = html.xpath("//table/descendant::tr")
                con_doc = []
                if box2:
                    for i in box2[1:]:
                        try:
                            e_rel={}
                            e_rel['appealName'] = stripper(i.xpath(".//th[1]/descendant::text()").get())
                            e_rel['recordType'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                            e_rel['startDate'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                            e_rel['process'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                            con_doc.append(e_rel)
                        except:
                            pass
                    each['allAppeals'] = con_doc
            except:
                print('failure')
                print('failure')
                print('failure')


            yield each
    def spider_closed(self, spider):
        self.driver.quit()
        self.drivera.quit()
        spider.logger.info("Spider closed: %s", spider.name)
      