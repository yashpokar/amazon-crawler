import scrapy


class Item(scrapy.Item):
    current_url = scrapy.Field()


class ListingItem(Item):
    asin = scrapy.Field()
    name = scrapy.Field()
    pdp_url = scrapy.Field()
    image = scrapy.Field()
    images = scrapy.Field()
    promotion = scrapy.Field()
    price = scrapy.Field()
    ratings = scrapy.Field()
    is_prime = scrapy.Field()
    reviews = scrapy.Field()
    brand_name = scrapy.Field()
    brand_url = scrapy.Field()
    suggested_price = scrapy.Field()
    best_seller = scrapy.Field()


class Review(Item):
    id = scrapy.Field()
    ratings = scrapy.Field()
    ratings_url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    image = scrapy.Field()
    author_profile = scrapy.Field()
    was_verified_purchase = scrapy.Field()
    body = scrapy.Field()
    date = scrapy.Field()
    helpful_votes = scrapy.Field()
