import scrapy


class PdpSpider(scrapy.Spider):
	name = 'pdp'
	allowed_domains = ['www.amazon.com']
	start_urls = ['https://www.amazon.com/dp/B073R6R3XY/?th=1&psc=1']

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
			questions_answered = response.xpath('//a[@id="askATFLink"]//text()').re_first(r'\d+(?:,\d+)?')
			availability = response.xpath('//*[@id="availability"]//text()').extract_first(default='')

			return_policy = response.xpath('//a[@id="creturns-policy-anchor-text"]//text()').extract()

			features = response.xpath('//*[@class="feature"]//text()').extract()
			fit_recommandations = response.xpath('//*[@id="fitRecommendationsLink"]/text()').extract_first(default='')
			fit_recommandations_link = response.xpath('//*[@id="fitRecommendationsLink"]/@href').extract_first(default='')
			color = response.xpath('//*[@id="variation_color_name"]//label[contains(text(), "Color:")]/../self::*[@class="selection"]/text()').extract_first()

			sizes = response.xpath('//*[@id="variation_size_name"]//option[not(contains(text(), "Select"))]/text()').extract()
			_colors = response.xpath('//li[contains(@id, "color_name_")]')

			colors = []

			for _color in _colors:
				colors.append({
					'name': _color.xpath('.//@title').extract_first(default=''),
					'asin': _color.xpath('.//@data-defaultasin').extract_first(default=''),
					'url': _color.xpath('.//@data-dp-url').extract_first(default=''),
				})

			seller_name = response.xpath('//*[@id="merchant-info"]//a[contains(@href, "/gp/help/seller")]/text()').extract_first(default='')
			seller_url = response.xpath('//*[@id="merchant-info"]//a[contains(@href, "/gp/help/seller")]/@href').extract_first(default='')
			seller_id = response.xpath('//*[@id="merchant-info"]//a[contains(@href, "/gp/help/seller")]/@href').re_first(r'&seller=([^&"]+)')
			seller_id = response.xpath('//input[@id="isMerchantExclusive"]/@value').extract_first()
			rsid = response.xpath('//input[@id="rsid"]/@value').extract_first()

			fbc_name = response.xpath('//*[@id="SSOFpopoverLink"]/text()').extract_first()
			fbc_url = response.xpath('//*[@id="SSOFpopoverLink"]/@href').extract_first()

			gift_wrap_available = response.xpath('//*[@id="merchant-info"]//*[contains(text(), "Gift-wrap available")]').extract_first(default='')

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
				'questions_answered': questions_answered,
				'sizes': sizes,
				'colors': colors,
				'color': color,
				'fbc_url': fbc_url,
				'fbc_name': fbc_name,
				'gift_wrap_available': gift_wrap_available,
			}
		except Exception as e:
			self.logger.error(e)
