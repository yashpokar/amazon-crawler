from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///amazon.db', echo=True)
Base = declarative_base()


class Category(Base):
	__tablename__ = 'categories'

	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=True)
	image = Column(String(2083), nullable=True)
	created_at = Column(DateTime, default=datetime.now())
	updated_at = Column(DateTime, onupdate=datetime.now())


class CategoryUrl(Base):
	__tablename__ = 'category_urls'

	id = Column(Integer, primary_key=True)
	name = Column(String(255), nullable=False)
	url = Column(String(2083), nullable=False)
	category_id = Column(Integer, ForeignKey('categories.id'))
	created_at = Column(DateTime, default=datetime.now())
	updated_at = Column(DateTime, onupdate=datetime.now())

	category = relationship('Category', back_populates='urls')


Category.urls = relationship('CategoryUrl', order_by=CategoryUrl.id, back_populates='category')


class Brand(Base):
	__tablename__ = 'brands'

	id = Column(Integer, primary_key=True)
	name = Column(String(68), nullable=False)
	url = Column(String(2083), nullable=False)
	created_at = Column(DateTime, default=datetime.now())
	updated_at = Column(DateTime, onupdate=datetime.now())


class Listing(Base):
	__tablename__ = 'listing'

	id = Column(Integer, primary_key=True)
	current_url = Column(String(2083), nullable=False)
	asin = Column(String(10), nullable=False)
	name = Column(String(255), nullable=False)
	pdp_url = Column(String(2083), nullable=False)
	image = Column(String(2083), nullable=False)
	price = Column(String(50), nullable=False)
	images = Column(ARRAY(String))
	promotion = Column(String)
	ratings = Column(String(50))
	is_prime = Column(Boolean)
	reviews = Column(String)
	brand_name = Column(String)
	brand_url = Column(String)
	created_at = Column(DateTime, default=datetime.now())
	updated_at = Column(DateTime, onupdate=datetime.now())


class PDP(Base):
	__tablename__ = 'pdp'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	price = Column(String, nullable=False)
	ratings = Column(String, nullable=False)
	reviews = Column(String, nullable=False)
	created_at = Column(DateTime, default=datetime.now())
	updated_at = Column(DateTime, onupdate=datetime.now())


if __name__ == '__main__':
	Base.metadata.create_all(engine)
