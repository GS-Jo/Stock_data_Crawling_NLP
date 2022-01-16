import scrapy
import re 
import pandas as pd
from stock.items import StockItem

class StockSpider(scrapy.Spider):
    name = "Stock"
    
    def start_requests(self):
        codes = pd.read_csv("/home/ubuntu/crawling_project/news/stock_code.csv")["ISU_SRT_CD"].tolist()
        urls = [f"https://finance.naver.com/item/news_news.nhn?code={code}&page=&sm=title_entity_id.basic" for code in codes]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)
            
    def parse(self, response):
        page_links = response.xpath('/html/body/div/table[2]/tr/td/a/@href').extract()
        last_page = re.findall('page=([0-9]{1,4})', page_links[-1])[0]
        stock_url = str(response.url)
        for page in range(1,int(last_page)+1):
            url = stock_url[:-25] + str(page) + stock_url[-25:]
            yield scrapy.Request(url, callback=self.parse_content1)  
    
    def parse_content1(self, response):
        links = response.xpath('/html/body/div/table[1]/tbody/tr/td[1]/a/@href').extract()
        for link in links:
            yield scrapy.Request("https://finance.naver.com/" + link, callback=self.parse_content2)
        
    def parse_content2(self, response):
        item = StockItem()
        item["title"] = response.xpath('//*[@id="content"]/div[2]/table/tbody/tr[1]/th/strong/text()').extract()
        item["news"] = response.xpath('//*[@id="content"]/div[2]/table/tbody/tr[2]/th/span/text()').extract()
        item["date"] = response.xpath('//*[@id="content"]/div[2]/table/tbody/tr[2]/th/span/span/text()').extract()
        item["news_link"] = response.url
        yield item    
