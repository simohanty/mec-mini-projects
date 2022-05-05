import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.xpath("span[@class='text']/text()").get(),
                'author': quote.xpath('span/small/text()').get(),
                'tags': quote.xpath(".//a[@class='tag']/text()").extract(),
            }

        next_page = response.xpath('//*[@class="next"]/a/@href').get()
        absolute_next_page_url = response.urljoin(next_page)

        if absolute_next_page_url is not None:
            yield scrapy.Request(absolute_next_page_url)