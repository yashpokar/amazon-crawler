from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags
from amazon.processors import filter_price_in


class DefaultItemLoader(ItemLoader):
	default_in_processor = MapCompose(remove_tags, unicode.strip)
	default_output_processor = TakeFirst()


class ListingItemLoader(DefaultItemLoader):
	is_prime_in = MapCompose(bool)

	price_in = filter_price_in

	images_in = MapCompose(lambda imgs: [img.split(' ')[0] for img in imgs.split(', ')])
	images_out = MapCompose(unicode.strip)

	# TODO :: Not tested
		# Test it and also improve xpath
		# Substitute all the posibilities
	promotion_out = Join('|')


class ReviewItemLoader(DefaultItemLoader):
	date_in = MapCompose(lambda x: x[3:] if len(x) >= 3 else x)
