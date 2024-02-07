from typing import Iterable
import scrapy
from scrapy.http import Request
def stripper(second):
    if second:
        second = second.replace('\r','').replace('\n','').replace('\t','').replace(":","").strip()
    return second
                
    
    
from re import *

# Define a function to convert a string to camel case
def camel_case(s):
    # Use regular expression substitution to replace underscores and hyphens with spaces,
    # then title case the string (capitalize the first letter of each word), and remove spaces
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    
    # Join the string, ensuring the first letter is lowercase
    return ''.join([s[0].lower(), s[1:]])



class SouthoxonSpider(scrapy.Spider):
    name = "southoxon"
    # allowed_domains = ["a.com"]
    # start_urls = ["https://a.com"]

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(url="https://data.southoxon.gov.uk/ccm/support/Main.jsp?MODULE=ApplicationRefList&TYPE=Application&APPTYPE=ALL&REF=&Submit=Search")
    def parse(self, response):
        links = response.xpath("//div[@class='rowdiv']/div/a/@href").getall()
        for i in links:
            abs_i = f'https://data.southoxon.gov.uk/ccm/support/{i}'
            yield scrapy.Request(url=abs_i,callback=self.parsedetails)

    def parsedetails(self,response):
        links = response.xpath("//div[@class='rowdiv']/descendant::a/@href").getall()
        for i in links:
            abs_i = f'https://data.southoxon.gov.uk/ccm/support/{i}'
            yield scrapy.Request(url=abs_i,callback=self.each)

    def each(self,response):
        each = {}
        reurl =response.url
        each['url'] = response.url
        sp = reurl.split('REF=')
        each['planning_number'] = sp[-1]
        table_hd = response.xpath("//div[@class='leftcelldiv']")
        for i in table_hd:
            first = i.xpath(".//descendant::text()").get()
            first=stripper(first)
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
            
            yield each
            


