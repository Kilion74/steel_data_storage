import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["anepmetall.kz"]
    start_urls = [f"https://anepmetall.kz/katalog/ocinkovannyj-metalloprokat/truba-otsinkovannaya/?page={i}" for i in
                  range(1, 909)]

    def parse(self, response):
        urls = response.xpath('//tbody[@class="products-table-list"]/tr')
        for url in urls:
            link = url.xpath(
                './/td[@class="d-block d-sm-table-cell products-table__name border-0 border-bottom-sm-1 pt-3 px-3 pb-0 p-sm-3 py-md-4"]/a/@href').get()
            yield scrapy.Request(url=link, callback=self.parse_product)

    def parse_product(self, response):
        # Извлечение информации с карточки товара
        title = response.xpath('//div[@class="col-12"]/h1/text()').get()
        photo = response.xpath(
            '//div[@class="col-12 col-md-5 col-lg-4 col-xl-4"]/img/@src').get()  # Примерный селектор для цены
        params = response.xpath(
            '//div[@class="col-12 col-lg-8 col-md-7"]/ul[@class="product-info list-unstyled ps-md-3 mb-4"]/li')
        charact = []
        for param in params:
            name = param.xpath('.//span')
            for lis in name:
                sun = lis.xpath('.//text()').get()
                charact.append(sun)

        yield {
            'title': title,
            'photo': ('https://anepmetall.kz/' + photo),
            'params': ' '.join(charact)
        }
