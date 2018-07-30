import re
import scrapy
import json
from scrapy.selector import Selector
from amazon.loaders import ListingItemLoader
from amazon.items import ListingItem


class ListingSpider(scrapy.Spider):
	name = 'listing'
	allowed_domains = ['www.amazon.com']
	custom_settings = {
		'ITEM_PIPELINES': {
			# 'amazon.pipelines.ListingPipeline': 1,
		}
	}
	start_urls = ['https://www.amazon.com/s/ref=lp_1045024_ex_n_4?rh=n%3A7141123011%2Cn%3A7147440011%2Cn\
	%3A1040660%2Cn%3A1045024%2Cn%3A2346727011&bbn=1045024&ie=UTF8&qid=1532894010']

	def parse(self, response):
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
				data = '[%s]' % str(response.body).replace('&&&', ',').strip(',')
				data = [item for item in json.loads(data) if item.has_key('centerBelowPlus')][0]['centerBelowPlus']['data']['value']
				products = Selector(text=data)

			for product in products.xpath('//*[contains(@id, "result_")]'):
				il = ListingItemLoader(ListingItem(), product)

				il.add_value('current_url', response.url)
				il.add_xpath('asin', './@data-asin')
				il.add_xpath('name', './/a[@title]/@title')
				il.add_xpath('pdp_url', './/a[@href][@title]/@href')
				il.add_xpath('image', './/img[@src]/@src')
				il.add_xpath('promotion', './/*[contains(@id,"BESTSELLER")]/@id | .//*[starts-with(name(),"h")][contains(@class,"sponsored")]/text()')
				il.add_xpath('price', './/span[@class= "a-offscreen"]/text() | .//span[@class="sx-price sx-price-large"]//text()')
				il.add_xpath('ratings', './/span[@class = "a-icon-alt"]/text() | .//i[contains(@class,"a-icon-star-small")][not(contains(@class,"prime"))]/@class')
				il.add_xpath('is_prime', './/i[contains(@class,"a-icon-prime")]/@class')
				il.add_xpath('reviews', './/a[contains(@href,"customerReviews")]//text() | .//span[contains(@class,"review")]//text()')

				yield il.load_item()
		except Exception as e:
			self.logger.error(e)
