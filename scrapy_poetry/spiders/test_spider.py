import scrapy


class QuotesSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):
        id = '99B364E80F0E20C2'
        urls = [
            "https://so.gushiwen.cn/nocdn/ajaxfanyi.aspx?id={}".format(id),
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = f'test.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')