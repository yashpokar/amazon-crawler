from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
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


class Listing(Base):
	__tablename__ = 'listing'

	id = Column(Integer, primary_key=True)
	current_url = Column(String(2083), nullable=False)
	asin = Column(String(10), nullable=False)
	name = Column(String(255), nullable=False)
	pdp_url = Column(String(2083), nullable=False)
	image = Column(String(2083), nullable=False)
	promotion = Column(String, nullable=False)
	price = Column(String(50), nullable=False)
	ratings = Column(String(50), nullable=False)
	is_prime = Column(Boolean, default=False)
	reviews = Column(String, nullable=False)
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


class Brand(Base):
	__tablename__ = 'brands'

	id = Column(Integer, primary_key=True)
	created_at = Column(DateTime, default=datetime.now())
	updated_at = Column(DateTime, onupdate=datetime.now())


class BolletPoint(Base):
	__tablename__ = 'bolletpoints'

	id = Column(Integer, primary_key=True)
	body = Column(String, nullable=False)
	created_at = Column(DateTime, default=datetime.now())
	updated_at = Column(DateTime, onupdate=datetime.now())


class Image(Base):
	__tablename__ = 'images'

	id = Column(Integer, primary_key=True)
	url = Column(String(2083), nullable=False)
	created_at = Column(DateTime, default=datetime.now())
	updated_at = Column(DateTime, onupdate=datetime.now())


if __name__ == '__main__':
	Base.metadata.create_all(engine)
