import scrapy


class CategoriesSpider(scrapy.Spider):
    name = 'categories'
    allowed_domains = ['www.amazon.com']

    custom_settings = {
        'ITEM_PIPELINES': {
            'amazon.pipelines.CategoriesPipeline': 1,
        }
    }

    start_urls = ['https://www.amazon.com/gp/site-directory/ref=nav_shopall_btn/']

    def parse(self, response):
        categories = response.xpath('//*[@class="fsdDeptBox"]')

        for category in categories:
            image = category.xpath('.//*[@class="fsdDeptFullImage"]/@src').extract_first(default='')
            name = category.xpath('.//*[@class="fsdDeptTitle"]/text()').extract_first(default='')

            _sub_categories = category.xpath('.//*[contains(@class, "fsdDeptLink")]')

            urls = []

            for _sub_category in _sub_categories:
                items = {}
                items['urls'] = _sub_category.xpath('./@href').extract_first()
                items['sub_category_name'] = _sub_category.xpath('./text()').extract_first()
                urls.append(items)

            yield {
                'name': name.encode('utf-8'),
                'image': image.encode('utf-8'),
                'urls': urls
            }
