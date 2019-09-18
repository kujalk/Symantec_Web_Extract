#Date - 12/9/2019
#Developer - K.Janarthanan
#scrapy runspider ./symantec_one_letter.py -o <sample.json, .csv>
#To retrieve malware details from symantec database and the description of the threat (For 1 letter)


import scrapy

class symantec_scraper(scrapy.Spider):

    name = "Symantec_Malware_DB"
    all_links=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    start_urls=['https://www.symantec.com/security-center/a-z/_1234567890']

    for i in all_links:
        one_link='https://www.symantec.com/security-center/a-z/'+i
        start_urls.append(one_link)

    def parse(self, response):
        
        rows=response.css("tbody > tr")

        for single_row in rows:
            malware=single_row.css("td > a::text").extract_first()
            link="https://www.symantec.com"+str(single_row.css("td > a::attr(href)").extract_first())
            category=str(single_row.css("td + td ::text").extract_first()).strip()
            print("Malware: "+malware+"\tCategory: "+category + "Link: "+link)
            answer={'Broad_Category': category,'Threat':malware,'Link':link}
            yield scrapy.Request(link,callback=self.parse_link,meta={'item': answer})
                            
        
    def parse_link(self,response):

        describe=str(response.css("#technicaldescription p::text").extract()).rstrip() 

        item = response.meta['item']
        item['Description'] = describe
        yield item 
          
  