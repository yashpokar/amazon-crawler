from sqlalchemy.orm import sessionmaker
from amazon.models import engine, Category, CategoryUrl, Listing


class PostgresPipeline(object):
	def open_spider(self, spider):
		self.session = sessionmaker(bind=engine)()

	def close_spider(self, spider):
		self.session.commit()
		self.session.close()

	def process_item(self, item, spider):
		try:
			model = self._process_item(item)
			self.session.add(model)
			self.session.commit()
		except:
			self.session.rollback()

		return item


class CategoriesPipeline(PostgresPipeline):
	def _process_item(self, item):
		category = Category(name=item['name'], image=item['image'])
		category.urls = map(lambda name, url: CategoryUrl(name=name, url=url), item['urls'].items())

		return category


class ListingPipeline(PostgresPipeline):
	def _process_item(self, item):
		return Listing(**dict(item))
