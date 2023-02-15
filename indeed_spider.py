import scrapy


class QuotesSpider(scrapy.Spider):
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
        'COOKIES_STORAGE': 'scrapy_cookies.storage.sqlite.SQLiteStorage',
        'COOKIES_SQLITE_DATABASE': ':memory:'
    }

    name = 'quotes'
    start_urls = [
        'https://es.indeed.com/jobs?q=rabbitmq&start=20',
    ]

    def parse(self, response):
        for quote in response.css('span.companyName'):
            yield {
                'companyName': quote.css('::text').get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
