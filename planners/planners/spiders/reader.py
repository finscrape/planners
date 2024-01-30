from typing import Iterable
import scrapy
from scrapy.http import Request
import requests
import requests
import json

from scrapy.selector import Selector

from re import sub

# Define a function to convert a string to camel case
def camel_case(s):
    # Use regular expression substitution to replace underscores and hyphens with spaces,
    # then title case the string (capitalize the first letter of each word), and remove spaces
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    
    # Join the string, ensuring the first letter is lowercase
    return ''.join([s[0].lower(), s[1:]])


class ReaderSpider(scrapy.Spider):
    name = "reader"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []
    
    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(url="https://www.ebay.com",method="GET")
    def parse(self, response):
        
        url = "https://planning.reading.gov.uk/fastweb_PL/results.asp"

        payload = "ApplicationNumber=&AddressPrefix=&Postcode=&CaseOfficer=&ParishName=&AreaTeam=&WardMember=&Consultant=&DateReceivedStart=&DateReceivedEnd=&DateDecidedStart=&DateDecidedEnd=&Locality=&AgentName=&ApplicantName=&ShowDecided=&Decision_Made=&DecisionDescription=&Sort1=FullAddressPrefix&Sort2=DateReceived+DESC&Submit=Search"
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '324',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ASPSESSIONIDSGRSDQBR=EBIBMFAALPNNIFJCOPMJPMBH; ASPSESSIONIDSGTQQDTS=HGOCOGIAJHHNAJOJONGJKBIN; ASPSESSIONIDSGTQQDTS=ONOCOGIADOFPBMIAAIIHLHFF',
        'Host': 'planning.reading.gov.uk',
        'Origin': 'https://planning.reading.gov.uk',
        'Referer': 'https://planning.reading.gov.uk/fastweb_PL/search.asp',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        page = Selector(text=response.text)
        links = page.xpath("//a[contains(text(),'View Details')]/@href").getall()
        self.listhref.extend(links)

        nxt = page.xpath("//a[contains(text(),'Next')]/@href").get()
        if nxt:
            
            id = 2
            while True:
                if id > 2541:
                    break

                url = f"https://planning.reading.gov.uk/fastweb_PL/results.asp?Scroll={id}&ApplicationNumber=&AddressPrefix=&Postcode=&CaseOfficer=&ParishName=&AreaTeam=&WardMember=&Consultant=&DateReceivedStart=&DateReceivedEnd=&DateDecidedStart=&DateDecidedEnd=&Locality=&AgentName=&ApplicantName=&ShowDecided=&Decision_Made=&DecisionDescription=&Sort1=FullAddressPrefix&Sort2=DateReceived+DESC&Submit=Search"

                payload = "Scroll={id}&ApplicationNumber=&AddressPrefix=&Postcode=&CaseOfficer=&ParishName=&AreaTeam=&WardMember=&Consultant=&DateReceivedStart=&DateReceivedEnd=&DateDecidedStart=&DateDecidedEnd=&Locality=&AgentName=&ApplicantName=&ShowDecided=&Decision_Made=&DecisionDescription=&Sort1=FullAddressPrefix&Sort2=DateReceived+DESC&Submit=Search"
                headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Cookie': 'ASPSESSIONIDSGRSDQBR=EBIBMFAALPNNIFJCOPMJPMBH; ASPSESSIONIDSGTQQDTS=JBPCOGIAAFPELBJMMFIPGBLE; ASPSESSIONIDSGTQQDTS=HHADOGIANAGLHFIDMEEPPGKH',
                'Host': 'planning.reading.gov.uk',
                'Referer': 'https://planning.reading.gov.uk/fastweb_PL/results.asp',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'Content-Type': 'application/json'
                }

                response = requests.request("GET", url, headers=headers, data=payload)

                page = Selector(text=response.text)
                links = page.xpath("//a[contains(text(),'View Details')]/@href").getall()
                self.listhref.extend(links)

                id += 1

                
        for i in self.listhref:
            abs_i =f'https://planning.reading.gov.uk/fastweb_PL/full{i}'
            yield scrapy.Request(url=abs_i,callback=self.parsedetails)

    def parsedetails(self,response):
        each = {}
        each['planningUrl'] = response.url
        table_hd = response.xpath("//tr/th")
        for i in table_hd:
            first = i.xpath(".//text()").get()
            if first:
                second = i.xpath(".//following-sibling::td/text()").getall()
                second = ''.join(second)
                
                second = second.replace('\r','').replace('\n','').replace('\t','').replace(":","").strip()
                

                try:
                    fir = camel_case(first)

                    each[fir] = second
                except:
                    each[first] = second

        yield each
        self.total.append(each)
        
              
   
