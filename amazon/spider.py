from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import Spider

from kafka import KafkaConsumer


class KafkaSpider(Spider):

	def _set_crawler(self, crawler):
		super(KafkaSpider, self)._set_crawler(crawler)

		self.consumer = KafkaConsumer('scrapy', bootstrap_servers=['127.0.0.1:9092'], group_id='listing')

		self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
		self.crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)
		self.log('Reading url from kafka consumer')

	def next_request(self):
		message = next(self.consumer)

		if not message:
			return

		return self.make_requests_from_url(str(message.value))

	def schedule_next_request(self):
		req = self.next_request()

		if req:
			self.crawler.engine.crawl(req, spider=self)

	def spider_idle(self):
		self.schedule_next_request()
		raise DontCloseSpider

	def item_scraped(self, *args, **kwargs):
		self.schedule_next_request()
