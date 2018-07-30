import scrapy


class PdpSpider(scrapy.Spider):
	name = 'pdp'
	allowed_domains = ['www.amazon.com']
	start_urls = ['https://www.amazon.com/FENSACE-Womens-Sleeveless-Summer-1703013/dp/B073R6R3XY/ref=lp_2346727011_1_5?s=apparel&ie=UTF8&qid=1532970616&sr=1-5&nodeID=2346727011&psd=1']

	def parse(self, response):
		try:
			_brand = response.xpath('//*[@id="bylineInfo"]')

			brand_name = _brand.xpath('./text()').extract_first(default='')
			brand_url = _brand.xpath('./@href').extract_first(default='')

			name = response.xpath('//*[@id="productTitle"]/text()').extract_first(default='')
			ratings = response.xpath('//i[contains(@class, "a-icon-star")]/span/text()').extract_first(default='')
			num_of_reviews = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first(default='')
			price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first(default='')
			bullet_points = response.xpath('//*[@id="feature-bullets"]//span[@class="a-list-item"]/text()').extract()
			images = response.xpath('//script[contains(text(), "ImageBlockATF")]')\
				.re(r'https:\/\/images-na.ssl-images-amazon.com\/images[^jpg]+.jpg')

			yield {
				'brand': {
					'name': brand_name,
					'url': brand_url,
				},
				'name': name,
				'price': price,
				'bullet_points': bullet_points,
				'images': images,
				'ratings': ratings,
				'num_of_reviews': num_of_reviews,
			}
		except Exception as e:
			self.logger.error(e)
