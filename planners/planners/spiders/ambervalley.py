from typing import Iterable
import scrapy
import requests
from scrapy.http import Request
from planners.util import dates_stry
from time import sleep
from scrapy import Selector
import json
class AmbervalleySpider(scrapy.Spider):
    name = "ambervalley"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def start_requests(self):
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):

        import requests

        url = "https://info.ambervalley.gov.uk/WebServices/AVBCFeeds/DevConJSON.asmx/PlanAppsAllValidNonDetermined"

        payload = "wardCode=&parishCode="
        headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '21',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        page = response.text
        try:
            html = json.loads(page)
        except:
            pass


        if html:
            for i in html:
                ref = i.get("refVal")
                ref = ref.replace("/",r"%2F")
                abs_i = f'https://info.ambervalley.gov.uk/WebServices/AVBCFeeds/DevConJSON.asmx/GetPlanAppDetails?refVal={ref}'
                yield scrapy.Request(url=abs_i,callback=self.details,meta={'ref':ref})
                sleep(1)
        


       
        start = 0
        
        for d in dates_stry[0:-1]:

            start += 1
            fd = d
            nd = dates_stry[start]
            url = "https://info.ambervalley.gov.uk/WebServices/AVBCFeeds/DevConJSON.asmx/PlanAppsDetermined"

            payload = f"wardCode=&parishCode=&fromDate={fd}&toDate={nd}"
            headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '59',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            page = response.text
            try:
                html = json.loads(page)
            except:
                continue


            if html:
                for i in html:
                    ref = i.get("refVal")
                    ref = ref.replace("/",r"%2F")
                    abs_i = f'https://info.ambervalley.gov.uk/WebServices/AVBCFeeds/DevConJSON.asmx/GetPlanAppDetails?refVal={ref}'
                    yield scrapy.Request(url=abs_i,callback=self.details,meta={'ref':ref})
                    sleep(1)
            

    def details(self,response):
        ref = response.meta['ref']
        page = response.body
        try:
            html = json.loads(page)
        except:
            pass

        if html:
            each = {}
            for key, value in html.items():

                each[key] = value
            yield scrapy.Request(url=f'https://info.ambervalley.gov.uk/WebServices/AVBCFeeds/DemocracyJSON.asmx/GetCommitteeDocsByPlanAppRef?refVal={ref}&publicOnly=true',callback=self.com,meta={'each':each,'ref':ref})

    def com(self,response):
        ref = response.meta['ref']
        each = response.meta['each']
        page = response.body
        try:
            html = json.loads(page)
        except:
            pass

        if html:
            
            each['committeeDoc'] = html
        yield scrapy.Request(url=f'https://info.ambervalley.gov.uk/WebServices/AVBCFeeds/IdoxEDMJSON.asmx/GetIdoxEDMDocListForCase?refVal={ref}&docApplication=planning',callback=self.idox,meta={'each':each,'ref':ref})

    def idox(self,response):
        ref = response.meta['ref']
        each = response.meta['each']
        page = response.body
        try:
            html = json.loads(page)
        except:
            pass

        if html:
            
            each['idoxEdmDocListForCase'] = html
        yield scrapy.Request(url=f'https://info.ambervalley.gov.uk/WebServices/AVBCFeeds/DevConJSON.asmx/GetApplicableConstraintsForPlanApp?refVal={ref}',callback=self.con,meta={'each':each,'ref':ref})

    def con(self,response):
        ref = response.meta['ref']
        each = response.meta['each']
        page = response.body
        try:
            html = json.loads(page)
        except:
            pass

        if html:
            
            each['applicableConstraints'] = html
        yield scrapy.Request(url=f'https://info.ambervalley.gov.uk/WebServices/AVBCFeeds/DevConJSON.asmx/GetConsultees?refVal={ref}&consulteeType=consultees',callback=self.consa,meta={'each':each,'ref':ref})

    def consa(self,response):
        ref = response.meta['ref']
        each = response.meta['each']
        page = response.body
        try:
            html = json.loads(page)
        except:
            pass

        if html:
            
            each['consultees'] = html
        yield scrapy.Request(url=f'https://info.ambervalley.gov.uk/WebServices/AVBCFeeds/DevConJSON.asmx/GetConsultees?refVal={ref}&consulteeType=pressList',callback=self.const,meta={'each':each,'ref':ref})

    def const(self,response):
        ref = response.meta['ref']
        each = response.meta['each']
        page = response.body
        try:
            html = json.loads(page)
        except:
            pass

        if html:
            
            each['consulteesTypePressList'] = html
        yield scrapy.Request(url=f'https://info.ambervalley.gov.uk/WebServices/AVBCFeeds/DevConJSON.asmx/GetConsultees?refVal={ref}&consulteeType=siteNotice',callback=self.consty,meta={'each':each,'ref':ref})

    def consty(self,response):
        ref = response.meta['ref']
        each = response.meta['each']
        page = response.body
        try:
            html = json.loads(page)
        except:
            pass

        if html:
            
            each['consulteesTypeSiteNotice'] = html
        yield scrapy.Request(url=f'https://info.ambervalley.gov.uk/WebServices/AVBCFeeds/DevConJSON.asmx/GetConsultees?refVal={ref}&consulteeType=neighbour',callback=self.conne,meta={'each':each,'ref':ref})

    def conne(self,response):
        ref = response.meta['ref']
        each = response.meta['each']
        page = response.body
        try:
            html = json.loads(page)
        except:
            pass

        if html:
            
            each['consulteesTypeNeighbours'] = html
        yield each
        

    
    