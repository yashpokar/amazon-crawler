from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags


class ListingItemLoader(ItemLoader):
	default_in_processor = MapCompose(remove_tags, unicode.strip)
	default_output_processor = TakeFirst()

	is_prime_in = MapCompose(bool)
