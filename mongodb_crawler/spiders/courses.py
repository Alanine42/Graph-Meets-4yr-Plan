import scrapy
from ..items import CourseItem
import re

class CoursesSpider(scrapy.Spider):
    name = 'courses'
    allowed_domains = ['catalog.ucsd.edu']
    # will append to courseObjects.json
    start_urls = ['https://catalog.ucsd.edu/courses/COGS.html', 'https://catalog.ucsd.edu/courses/DSC.html', 'https://catalog.ucsd.edu/courses/HUM.html'] 

    def parse(self, response):
        names = response.xpath("//p[@class='course-name']/text()").getall()
        namesItr = iter(names)
        descriptions = response.xpath("//p[@class='course-descriptions']//text()").getall()


        currCourse = None
        readingPrereqs = False
        for des in descriptions:
            
            if des in {'Prerequisites:', 'Prerequisites: ', ' '}:
                readingPrereqs = True
                continue
            
            if readingPrereqs:
                currCourse['prereqRaw'] = des
                readingPrereqs = False
                continue
            
            # export the previous object
            if currCourse:
                yield currCourse
            
            currCourse = CourseItem()
            currCourse['cDescription'] = des
            
            name = next(namesItr)
            cID = re.search("(.+)\.", name).groups()[0]
            currCourse['cID'] = cID
            currCourse['cName'] = name
            
            
            
            
                        
