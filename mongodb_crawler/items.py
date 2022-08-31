# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    author = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()
    
    
class CourseItem(scrapy.Item):
    cID = scrapy.Field()    # "CSE 120"
    cName = scrapy.Field()  # "CSE 110. Software Engineering"
    cDescription = scrapy.Field()   # does not include prerequisite parts
    prereqRaw = scrapy.Field()
    
    pass    
