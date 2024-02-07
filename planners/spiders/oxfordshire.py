import scrapy

from typing import Iterable
import scrapy
from scrapy.http import Request
import requests
import requests
import json

from scrapy.selector import Selector

from re import sub

# Define a function to convert a string to camel case
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

class OxfordshireSpider(scrapy.Spider):
    name = "oxfordshire"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def __init__(self, name=None, **kwargs):
        self.listhref  = []
        self.plan = []
        self.total = []
    
    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(url="https://www.ebay.com",method="GET")

    def parse(self,response):
        import requests

        url = "https://myeplanning.oxfordshire.gov.uk/Search/Results/1/50"

        payload = {}
        headers = {
        'authority': 'myeplanning.oxfordshire.gov.uk',
        'method': 'GET',
        'scheme': 'https',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': 'occ_gdpr_settings={%22necessaryCookies%22:[%22%22]%2C%22consentDate%22:1704546432000%2C%22interactedWith%22:true%2C%22analytics%22:true%2C%22thirdParties%22:true%2C%22consentExpiry%22:365%2C%22user%22:%227932C037-AEEC-4E6D-ABB2-7A0E91F39060%22}; google_stats=true; third_party=true; _hjSessionUser_2968655=eyJpZCI6IjdkZGUwZDIyLWYwMjMtNTQzMC1hNjliLTMyYTU4MDlhOGQ4OCIsImNyZWF0ZWQiOjE3MDQ1NTAwMzUyODcsImV4aXN0aW5nIjp0cnVlfQ==; _gcl_au=1.1.832424665.1704550035; _ga=GA1.1.1866295132.1704550036; _hjIncludedInSessionSample_2968655=1; _hjSession_2968655=eyJpZCI6ImZlNmFiZGZlLTQzY2ItNDQ0ZC04MjNiLWUxMGE1ZjFkYzZjMiIsImMiOjE3MDU4ODIxODM1MjAsInMiOjEsInIiOjAsInNiIjoxLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _ga_6M6QEB5TB7=GS1.1.1705882183.2.1.1705882192.0.0.0; AcceptedDisclaimer=22/01/2024 01:09:57; ASP.NET_SessionId=5ulhls3vhahdjnadrdaw3ytv; __RequestVerificationToken=VMaJfwRp_9YXUQYCV7KxcQBlv7vCjt-W2F-_Tb2pbbH7JSMsDmon3NHeOYujFHRvuMTIkBD8V7T9vPcMHCKSwEP8QRmWOlnW9Uwi3M8HoyQ1'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        page = Selector(text=response.text)
        links = page.xpath("//td[@class='occlss-table__cell app-no-column left-margin']/a/@href").getall()
        self.listhref.extend(links)
        
        
        nxt = page.xpath("//a[@aria-label='Next Page.']/@href").get()
        if nxt:
            
            id = 2
            while True:
                if id > 54:
                    break

                url = f"https://myeplanning.oxfordshire.gov.uk/Search/Results/{id}/50"

                payload = {}
                headers = {
                'authority': 'myeplanning.oxfordshire.gov.uk',
                'method': 'GET',
                'scheme': 'https',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cookie': 'occ_gdpr_settings={%22necessaryCookies%22:[%22%22]%2C%22consentDate%22:1704546432000%2C%22interactedWith%22:true%2C%22analytics%22:true%2C%22thirdParties%22:true%2C%22consentExpiry%22:365%2C%22user%22:%227932C037-AEEC-4E6D-ABB2-7A0E91F39060%22}; google_stats=true; third_party=true; _hjSessionUser_2968655=eyJpZCI6IjdkZGUwZDIyLWYwMjMtNTQzMC1hNjliLTMyYTU4MDlhOGQ4OCIsImNyZWF0ZWQiOjE3MDQ1NTAwMzUyODcsImV4aXN0aW5nIjp0cnVlfQ==; _gcl_au=1.1.832424665.1704550035; _ga=GA1.1.1866295132.1704550036; _hjIncludedInSessionSample_2968655=1; _hjSession_2968655=eyJpZCI6ImZlNmFiZGZlLTQzY2ItNDQ0ZC04MjNiLWUxMGE1ZjFkYzZjMiIsImMiOjE3MDU4ODIxODM1MjAsInMiOjEsInIiOjAsInNiIjoxLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _ga_6M6QEB5TB7=GS1.1.1705882183.2.1.1705882192.0.0.0; AcceptedDisclaimer=22/01/2024 01:09:57; ASP.NET_SessionId=5ulhls3vhahdjnadrdaw3ytv; __RequestVerificationToken=VMaJfwRp_9YXUQYCV7KxcQBlv7vCjt-W2F-_Tb2pbbH7JSMsDmon3NHeOYujFHRvuMTIkBD8V7T9vPcMHCKSwEP8QRmWOlnW9Uwi3M8HoyQ1'
                }

                response = requests.request("GET", url, headers=headers, data=payload)

                page = Selector(text=response.text)
                links = page.xpath("//td[@class='occlss-table__cell app-no-column left-margin']/a/@href").getall()
                self.listhref.extend(links)
                
                id += 1

        for i in self.listhref:
            abs_i =f'https://myeplanning.oxfordshire.gov.uk{i}'
            
        
            url = abs_i
            payload = {}
            headers = {
            'authority': 'myeplanning.oxfordshire.gov.uk',
            'method': 'GET',
            'scheme': 'https',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'occ_gdpr_settings={%22necessaryCookies%22:[%22%22]%2C%22consentDate%22:1704546432000%2C%22interactedWith%22:true%2C%22analytics%22:true%2C%22thirdParties%22:true%2C%22consentExpiry%22:365%2C%22user%22:%227932C037-AEEC-4E6D-ABB2-7A0E91F39060%22}; google_stats=true; third_party=true; _hjSessionUser_2968655=eyJpZCI6IjdkZGUwZDIyLWYwMjMtNTQzMC1hNjliLTMyYTU4MDlhOGQ4OCIsImNyZWF0ZWQiOjE3MDQ1NTAwMzUyODcsImV4aXN0aW5nIjp0cnVlfQ==; _gcl_au=1.1.832424665.1704550035; _ga=GA1.1.1866295132.1704550036; _hjIncludedInSessionSample_2968655=1; _hjSession_2968655=eyJpZCI6ImZlNmFiZGZlLTQzY2ItNDQ0ZC04MjNiLWUxMGE1ZjFkYzZjMiIsImMiOjE3MDU4ODIxODM1MjAsInMiOjEsInIiOjAsInNiIjoxLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _ga_6M6QEB5TB7=GS1.1.1705882183.2.1.1705882192.0.0.0; AcceptedDisclaimer=22/01/2024 01:09:57; ASP.NET_SessionId=5ulhls3vhahdjnadrdaw3ytv; __RequestVerificationToken=VMaJfwRp_9YXUQYCV7KxcQBlv7vCjt-W2F-_Tb2pbbH7JSMsDmon3NHeOYujFHRvuMTIkBD8V7T9vPcMHCKSwEP8QRmWOlnW9Uwi3M8HoyQ1'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            page = Selector(text=response.text)

            each = {}
            each['planningUrl'] = abs_i

            titlee = page.xpath("//h1[contains(text(),'Planning')]/text()").get()
            if titlee:
                titlee = titlee.replace("Planning application:","")

            each['planningApplication'] = titlee

            table_hd = page.xpath("//h2[contains(@class,'occlss-form-cntrls__label')]")
            for i in table_hd:
                first = i.xpath(".//text()").get()
                if first:
                    second = i.xpath(".//following-sibling::div/p/text()").getall()
                    second = ''.join(second)
                    
                    second = stripper(second)

                    try:
                        fir = camel_case(first)

                        each[fir] = second
                    except:
                        each[first] = second

            nei_doc = []
            rd = page.xpath("//table[@id='documentTable']/descendant::tr")
            if rd:
                for i in rd[1:]:
                    e_rel={}
                    e_rel['description'] = stripper(i.xpath(".//td[2]/descendant::text()").get())
                    e_rel['documentPlan'] = stripper(i.xpath(".//td[3]/descendant::text()").get())
                    e_rel['dateAdded'] = stripper(i.xpath(".//td[4]/descendant::text()").get())
                    file_link = stripper(i.xpath(".//td[5]/descendant::a/@href").get())
                    if file_link:
                        e_rel['download'] ='https://myeplanning.oxfordshire.gov.uk/' + file_link
                    nei_doc.append(e_rel)
                
            if nei_doc:
                each['documents'] = nei_doc


            yield each
            self.total.append(each)
            
                
    
