from sqlalchemy.orm import sessionmaker
from amazon.models import engine, Category, CategoryUrl, Listing


class PostgresPipeline(object):
	items = []
	batch_size = 100

	def open_spider(self, spider):
		self.session = sessionmaker(bind=engine)()

	def close_spider(self, spider):
		self.dump_into_db()
		self.session.close()

	def process_item(self, item, spider):
		model = self._process_item(item)
		self.items.append(model)

		if self.is_batch_completed():
			self.dump_into_db()

		return item

	def dump_into_db(self):
		self.session.add_all(self.items)
		self.session.commit()
		self.items = []

	def is_batch_completed(self):
		return len(self.items) > 100



class CategoriesPipeline(PostgresPipeline):
	def _process_item(self, item):
		category = Category(name=item['name'], image=item['image'])

		for url in item['urls']:
			category.urls.append(CategoryUrl(name=url['name'], url=url['url']))

		return category


class ListingPipeline(PostgresPipeline):
	def _process_item(self, item):
		return Listing(**dict(item))
