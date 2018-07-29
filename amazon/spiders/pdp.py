import scrapy


class PdpSpider(scrapy.Spider):
	name = 'pdp'
	allowed_domains = ['www.amazon.com']
	start_urls = ['http://www.amazon.com/AUSELILY-Sleeveless-Pockets-T-Shirt-Dresses/dp/\
		B06XSBSKMG/ref=lp_2346727011_1_1?s=apparel&ie=UTF8&qid=1530795986&sr=1-1&nodeID=2346727011&psd=1/']

	def parse(self, response):
		_brand = response.xpath('//*[@id="bylineInfo"]')

		brand_name = _brand.xpath('./text()')
		brand_url = _brand.xpath('./@href')

		name = response.xpath('//*[@id="productTitle"]/text()')
		ratings = response.xpath('//i[contains(@class, "a-icon-star")]/span/text()')
		num_of_reviews = response.xpath('//*[@id="acrCustomerReviewText"]/text()')

		price = response.xpath('//*[@id="priceblock_ourprice"]/text()')

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
