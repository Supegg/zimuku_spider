import scrapy
from mySpider.items import RunoobItem

class RunoobSpider(scrapy.Spider):
    name = 'runoob'
    allowed_domains = ['runoob.com']
    start_urls = []

    def start_requests(self):
        ua={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like GeChrome/63.0.3239.84 Safari/537.36'}
        yield scrapy.http.Request('https://www.runoob.com/w3cnote/scrapy-detail.html',headers=ua)

    def parse(self, response):
        ul = response.xpath('/html/body/div[3]/div/div[1]/div/div[2]/div/ul[1]')   
        
        noob = RunoobItem()
        noob['flows'] = list()
        for li in response.xpath('/html/body/div[3]/div/div[1]/div/div[2]/div/ul[2]/li'):
            noob['flows'].append(li.xpath('text()').extract()[0].strip())

        # print(noob)
        noob['file_urls'] = ['https://www.runoob.com/wp-content/uploads/2018/12/20180726180149969.png']
        noob['image_urls'] = ['https://www.runoob.com/wp-content/uploads/2018/12/20180726180149969.png']
        return noob
