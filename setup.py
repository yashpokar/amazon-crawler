from setuptools import setup, find_packages

setup(
    name='amazon',
    version='0.0.1',
	description='',
	packages=find_packages(),
    install_requires=[
        'scrapy',
        'SQLAlchemy',
        'psycopg2-binary',
        'scrapyd',
        'pymongo',
    ]
)
