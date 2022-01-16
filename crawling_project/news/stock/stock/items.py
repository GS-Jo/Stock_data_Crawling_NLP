import scrapy


class StockItem(scrapy.Item):
    title = scrapy.Field()
    news = scrapy.Field()
    news_link = scrapy.Field()
    date = scrapy.Field()
    
