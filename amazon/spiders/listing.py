import re
import scrapy
import json
from scrapy.selector import Selector
from amazon.loaders import ListingItemLoader
from amazon.items import ListingItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class ListingSpider(scrapy.Spider):
	name = 'listing'

	custom_settings = {
		'ITEM_PIPELINES': {
			'amazon.pipelines.ListingPipeline': 1,
		}
	}

	def start_requests(self):
		with open('urls.txt', 'r') as f:
			urls = f.read().split('\n')

			for url in urls:
				if url:
					url = self.removeUnnecessary('https://www.amazon.com{}'.format(url))
					yield scrapy.Request(url, callback=self.parse, errback=self.errback_httpbin)

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
						yield response.follow(self.removeUnnecessary(next_page), meta={ 'is_pagination_done': True })
			else:	
				data = '[%s]' % str(response.body).replace('&&&', ',').strip(',')
				data = [item for item in json.loads(data) if item.has_key('centerBelowPlus')][0]['centerBelowPlus']['data']['value']
				products = Selector(text=data)
			
			products = products.xpath('//*[contains(@id, "result_")]')

			if len(products) != 48:
				self.logger.info('got only %s products from page %s' % (len(products), response.url))

			for product in products:
				il = ListingItemLoader(ListingItem(), product)

				il.add_value('current_url', response.url)
				il.add_xpath('asin', './@data-asin')
				il.add_xpath('name', './/a[@title]/@title')
				il.add_xpath('pdp_url', './/a[@href][@title]/@href')
				il.add_xpath('image', './/img[@src]/@src')
				il.add_xpath('images', './/img[@src]/@srcset')
				il.add_xpath('promotion', './/i[contains(@class, "a-icon-addon")][contains(@class, "aok-align-bottom")]/text() | .//i[contains(@class, "a-icon-addon")][contains(@class, "pantry-promo-badge-orange")]/text()')

				il.add_xpath('price', './/span[@class= "a-offscreen"]/text()')
				il.add_xpath('price', 'concat(.//span[@class="sx-price-whole"]/text(), ".", .//sup[@class="sx-price-fractional"]/text())')
				il.add_xpath('ratings', './/i[contains(@class, "a-icon-star")]/span[@class="a-icon-alt"]/text()')
				il.add_xpath('is_prime', './/i[contains(@class,"a-icon-prime")]/@class')
				il.add_xpath('reviews', './/a[contains(@href,"customerReviews")]//text() | .//span[contains(@class,"review")]//text()')
				il.add_xpath('brand_name', './/span[@class="a-color-secondary s-overflow-ellipsis s-size-mild"]/text()')
				il.add_xpath('brand_url', './/span[@class="a-color-secondary s-overflow-ellipsis s-size-mild"]/../self::*/@href')
				il.add_xpath('suggested_price', './/span[contains(@aria-label, "Suggested Retail Price:")]/@aria-label')
				il.add_xpath('best_seller', './/span[contains(@id, "BESTSELLER_")]//span[@class="a-badge-text"]/text()')

				yield il.load_item()
		except Exception as e:
			self.logger.error(e)

	def removeUnnecessary(self, url):
		return re.sub(r'&qid=\d+', '', url)

	def errback_httpbin(self, failure):
		# log all failures
		self.logger.error(repr(failure))

		# in case you want to do something special for some errors,
		# you may need the failure's type:

		if failure.check(HttpError):
			# these exceptions come from HttpError spider middleware
			# you can get the non-200 response
			response = failure.value.response
			self.logger.error('HttpError on %s', response.url)

		elif failure.check(DNSLookupError):
			# this is the original request
			request = failure.request
			self.logger.error('DNSLookupError on %s', request.url)

		elif failure.check(TimeoutError, TCPTimedOutError):
			request = failure.request
			self.logger.error('TimeoutError on %s', request.url)
