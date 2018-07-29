import scrapy


class ListingItem(scrapy.Item):
    asin = scrapy.Field()
    name = scrapy.Field()
    pdp_url = scrapy.Field()
    current_url = scrapy.Field()
    img_url = scrapy.Field()
    promotion = scrapy.Field()
    price = scrapy.Field()
    ratings = scrapy.Field()
    is_prime = scrapy.Field()
    reviews = scrapy.Field()
