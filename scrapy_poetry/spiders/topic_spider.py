import scrapy


class QuotesSpider(scrapy.Spider):
    name = "topics"

    def start_requests(self):
        urls = [
            'https://so.gushiwen.cn/gushi/huaigu.aspx',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = "怀古"
        filename = f'topic-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')