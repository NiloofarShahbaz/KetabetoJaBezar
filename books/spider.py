import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self,search_parameter):
        super().__init__()
        self.search_parameter=search_parameter
        self.search_parameter=self.search_parameter.replace(' ','+')


    def start_requests(self):
        print('searchchchhhhhhhhhh',self.search_parameter)
        urls = [
            'https://www.google.com/search?client=ubuntu&channel=fs&q='+self.search_parameter+'&ie=utf-8&oe=utf-8'
        ]
        for url in urls:
            for i in range(10):
                yield scrapy.Request(url=url + str(i * 10), callback=self.parse)

    def parse(self, response):
        a = response.xpath("//div/h3/a/@href").extract()
        file=open('search_results.txt','a')
        for item in a:
            item=item.replace('/url?q=','')
            #print(item)
            file.write(item)
            file.write('\n')
        file.close()



