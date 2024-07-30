import scrapy

class CyberSpiderSpider(scrapy.Spider):
    name = "cyber_spider"
    allowed_domains = ["cybernews.com"]
    start_urls = ["https://cybernews.com/news/"]

    def parse(self, response):
        # Scraping news articles
        news = response.css('div.cells__item_width')
        for new in news:
            title = new.css('.heading_size_4::text').get()
            relative_url = new.css('a::attr(href)').get()
            title_link = response.urljoin(relative_url)
            published_date = new.css('.prefix::text').get()
            
            
            yield scrapy.Request(url=title_link, callback=self.parse_article, meta={'title': title, 'published_date': published_date})

       
        next_page = response.css('a.pagination__number[href]:contains("Next")::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        
    def parse_article(self, response):
        title = response.meta['title']
        published_date = response.meta['published_date']
        
        text_elements = response.xpath("//div[@class='content']//text()").getall()
        text = ' '.join(text_elements).strip().replace('\n', '')
        yield {
            'title': title,
            'published_date': published_date,
            'description': text
        }
