import re
import scrapy
from scrapy.selector import Selector
from amazon.loaders import ListingItemLoader
from amazon.items import ListingItem


class ListingSpider(scrapy.Spider):
	name = 'listing'

	custom_settings = {
		'ITEM_PIPELINES': {
			# 'amazon.pipelines.ListingPipeline': 1,
		},
		'DOWNLOADER_MIDDLEWARES': {
			# 'amazon.middlewares.ProxyMiddleware': 1
		}
	}

	def start_requests(self):
		with open('urls.txt', 'r') as f:
			urls = f.read().split('\n')

			for url in urls:
				if url:
					yield scrapy.Request('https://www.amazon.com{}'.format(url))

	def parse(self, response):
		title = response.xpath('//title/text()').extract_first()

		try:
			products = response

			if not response.meta.get('is_pagination_done', False):
				last_page = response.xpath('//*[@class="pagnDisabled"]/text()').extract_first(default=0)
				next_page = response.xpath('//*[@id="pagnNextLink"]/@href').extract_first(default='')
				last_page = int(last_page)

				base_url = 'https://www.amazon.com/mn/search/ajax/'

				if next_page and last_page:
					for page in range(2, int(last_page) + 1):
						next_page = re.sub(r'&page=\d+', '&page={}'.format(page), next_page)
						next_page = next_page\
							.replace('/s/', base_url)\
							.replace('/gp/', base_url)
						yield response.follow(next_page, meta={ 'is_pagination_done': True })
			else:
				products = re.findall(r'&&&\n{\s*\n*[^"]*"centerBelowPlus" : {\n*.+\n*\n*\s*.*\n*\s*.+\n*\n*[^"value"]+"value" : (.+)"', response.body)[0]
				products = Selector(text=products.replace('\\"', '"'))

			for product in products.xpath('//*[contains(@id, "result_")]'):
				il = ListingItemLoader(ListingItem(), product)

				il.add_value('current_url', response.url)
				il.add_xpath('asin', './@data-asin')
				il.add_xpath('name', './/a[@title]/@title')
				il.add_xpath('pdp_url', './/a[@href][@title]/@href')
				il.add_xpath('image', './/img[@src]/@src')
				il.add_xpath('images', './/img[@src]/@srcset')
				il.add_xpath('promotion', './/*[contains(@id,"BESTSELLER")]/@id | .//*[starts-with(name(),"h")][contains(@class,"sponsored")]/text()')
				il.add_xpath('price', './/span[@class= "a-offscreen"]/text() | .//span[@class="sx-price sx-price-large"]//text()')
				il.add_xpath('ratings', './/i[contains(@class, "a-icon-star")]/span[@class="a-icon-alt"]/text()')
				il.add_xpath('is_prime', './/i[contains(@class,"a-icon-prime")]/@class')
				il.add_xpath('reviews', './/a[contains(@href,"customerReviews")]//text() | .//span[contains(@class,"review")]//text()')
				il.add_xpath('brand_name', './/span[@class="a-color-secondary s-overflow-ellipsis s-size-mild"]/text()')
				il.add_xpath('brand_url', './/span[@class="a-color-secondary s-overflow-ellipsis s-size-mild"]/../self::*/@href')

				yield il.load_item()
		except Exception as e:
			self.logger.error(e)
