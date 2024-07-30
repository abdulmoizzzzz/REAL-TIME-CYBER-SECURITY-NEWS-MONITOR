import scrapy

class InfoSpiderSpider(scrapy.Spider):
    name = "info_Spider"
    allowed_domains = ["www.infosecurity-magazine.com"]
    start_urls = ["https://www.infosecurity-magazine.com/news/"]

    def parse(self, response):
        news_items = []
        news = response.css('.webpage-item')
        for new in news:
            title = new.css('.webpage-title a::text').get()
            title_link = new.css('.webpage-title a::attr(href)').get()
            date = new.css('span.webpage-meta > time::attr(datetime)').get()

          
            news_item = {
                'title': title,
                'title_link': title_link,
                'date': date
            }

       
            yield scrapy.Request(url=title_link, meta={'news_item': news_item}, callback=self.parse_article)

       
        next_page = response.css('div.pagination > a[rel="next"]::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_article(self, response):
     
        news_item = response.meta['news_item']
        description = response.xpath("//div[@class='page-content']//p/text()").getall()
        combined_data = {**news_item, 'description': description}

        yield combined_data
