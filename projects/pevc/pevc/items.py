# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PevcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    data_type = scrapy.Field()
    suburb = scrapy.Field()
    state = scrapy.Field()
    postcode = scrapy.Field()
    img_src = scrapy.Field()
    preferred_mailing = scrapy.Field()
    phone = scrapy.Field()
    member_type = scrapy.Field()
    category = scrapy.Field()
    website = scrapy.Field()
    services_provided = scrapy.Field()
    social_profiles = scrapy.Field()
    hashstr = scrapy.Field()
    retrieval_data = scrapy.Field()
