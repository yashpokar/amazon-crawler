import scrapy
from scrapy.selector import Selector
from amazon.loaders import ReviewItemLoader
from amazon.items import Review


class ReviewsSpider(scrapy.Spider):
	name = 'reviews'
	allowed_domains = ['www.amazon.com']

	def start_requests(self):
		return [scrapy.FormRequest('http://www.amazon.com/hz/reviews-render/ajax/reviews/get/ref=cm_cr_othr_d_paging_btm_next_2/',
			formdata={
			'sortBy': '',
			'reviewerType': 'all_reviews',
			'formatType': '',
			'mediaType': '',
			'filterByStar': 'positive',
			'pageNumber': '1',
			'filterByKeyword': '',
			'shouldAppend': 'undefined',
			'deviceType': 'desktop',
			'reftag': 'cm_cr_othr_d_paging_btm_next_2',
			'pageSize': '50',
			'asin': 'B06XS25QHQ',
			'scope': 'reviewsAjax1'})]

	def parse(self, response):
		items = eval('[%s]' % response.body.replace('&&&', ',').strip(','))

		update = [item for item in items if item[0] == 'update'][0]
		reviews = [item[-1] for item in items if item[0] == 'append']

		for review in reviews:
			il = ReviewItemLoader(Review(), Selector(text=review))

			il.add_value('current_url', response.url)
			il.add_xpath('ratings', '//*[@data-hook="review-star-rating"]//text()')
			il.add_xpath('ratings_url', '//*[@class="a-link-normal"][contains(@title, "stars")]/@href')
			il.add_xpath('title', '//*[@data-hook="review-title"]/text()')
			il.add_xpath('author', '//a[@data-hook="review-author"][contains(@class, "author")]/text()')
			il.add_xpath('author_profile', '//a[@data-hook="review-author"][contains(@class, "author")]/@href')
			il.add_xpath('date', '//*[@data-hook="review-date"]/text()')
			il.add_xpath('was_verified_purchase', '//*[contains(text(), "Verified Purchase")]/text()')
			il.add_xpath('body', '//*[@data-hook="review-body"]/text()')
			il.add_xpath('image', '//img[@data-hook="review-image-tile"]/@src')
			il.add_xpath('helpful_votes', '//*[@data-hook="helpful-vote-statement"]/text()')

			yield il.load_item()
