from sqlalchemy.orm import sessionmaker
from amazon.models import engine, Category, CategoryUrl, Listing


class PostgresPipeline(object):
	def open_spider(self, spider):
		self.session = sessionmaker(bind=engine)()

	def close_spider(self, spider):
		self.session.close()

	def process_item(self, item, spider):
		model = self._process_item(item)
		self.session.add(model)
		self.session.commit()

		return item


class CategoriesPipeline(PostgresPipeline):
	def _process_item(self, item):
		category = Category(name=item['name'], image=item['image'])

		for url in item['urls']:
			category.urls.append(CategoryUrl(name=url['name'], url=url['url']))

		return category


class ListingPipeline(PostgresPipeline):
	def _process_item(self, item):
		return Listing(**dict(item))
