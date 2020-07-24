from scrapy import Spider, Request
from kicktraq.items import KicktraqItem
import re

class KicktraqSpider(Spider):
    name = 'kicktraq_spider'
    allowed_urls = ['https://www.kicktraq.com']
    start_urls = ['https://www.kicktraq.com/archive/?page=1']
    # need to write portion to iterate through pages 1-700

    def parse(self, response):
        total_pages =  700 # the archive doesn't go further than that
        url_list = [f'https://www.kicktraq.com/archive/?page={i+1}' for i in range(total_pages)]
        for url in url_list:
            yield Request(url = url, callback = self.parse_projects)

    def parse_projects(self, response):
        projects = response.xpath('//div[@class="project-infobox"]') # goes to infobox that contains h2 project-cat and project-infobits
        
        # looping through each project infobox for the items
        for project in projects:
            names = project.xpath('./h2/a/text()').extract_first() # getting project name 
            # print('='*50) # debugging and status check
            # print(">>> project name:", names)
            # print('='*50)
            
            category = project.xpath('./div[@class="project-cat"]/a/@href').extract() #project-cat href as string
            # checking if category has sub/category, assigning first el in category list to main_category, and first and second (if present) to category 
            main_category = ''
            if len(category) == 1:
                main_category = category[0].strip('/').replace('categories/','')
                category = None
            else:
                main_category = category[0].strip('/').replace('categories/','')
                category = category[1].strip('/').replace('categories/','').replace('/','|')

            # entire contents of details - will extract start times and deadlines in python from text    
            proj_details = project.xpath('.//div[@class="project-details"]//text()').extract() 
            
            # 
            try:
                money = project.xpath('.//div[@class="project-details"]//text()[2]').extract_first() 
                currency, pledged, goal = [s.replace(',', '') for s in [str(el) for el in re.findall(' (.)(.*) of .(.*) ' , money)[0]]]
                goal = int(goal)
                pledged = int(pledged)
            except Exception as e:
                currency = None
                goal = None
                pledged = None

            # try:
            #     dates = project.xpath('.//div[@class="project-details"]//text()').extract() #extracting all text in list of strings

            #     year = list(chain(*[re.findall('\((\d*)\)', date) for date in dates]))[0]
            #     # year = [re.findall('\((\d*)\)', date) for date in dates] #iterating over list of strings('dates') to find year
            #     # year = ''.join(list(chain(*year))) #flattening list and joining elements to get string

            #     start = [[el for el in re.findall('Dates: (\D*) (\d*)..', date)] for date in dates]
            #     start_month, start_day = list(chain(*start))[0]

            #     start_date = '-'.join([year, start_month, start_day])

            #     end_month, end_day = [[el for el in re.findall(' -> (\D*) (\d*)', date)[0]] for date in dates]
            #     deadline = '-'.join([year, end_month, end_day])
            # except Exception as e:
            #     dates = None
            #     start_date = None
            #     deadline = None

            try:
                backers = project.xpath('.//div[@class="project-details"]/text()[1]').extract_first()
                backers = int(re.findall('Backers: (\d*)', backers)[0])
            except Exception as e:
                backers = None

            status = project.xpath('.//div[@class="project-pledgilizer"]//h5/text()').extract_first()

            description = project.xpath('./div[1]/text()').extract_first()



            item = KicktraqItem()
            item['names'] = names
            item['category'] = category
            item['main_category'] = main_category
            item['proj_details'] = proj_details
            item['currency'] = currency
            item['goal'] = goal
            item['pledged'] = pledged
            # item['dates'] = dates
            # item['start_date'] = start_date
            # item['deadline'] = deadline
            item['backers'] = backers
            item['status'] = status
            item['description'] = description
            # item['year'] = year
            # item['start_day'] = start_day
            yield item
# '/categories/fashion/'.strip('/categories/')
# '/categories/fashion/accessories/'.remove('/categories/')
        # for name in names:
        #     item = KicktraqItem()
        #     item['name'] = name
    # currency = currency.Field() #need to take first element translate with https://transferwise.com/gb/blog/world-currency-symbols might need to scrape
    # deadline = deadline.Field()
    # goal = goal.Field()
    # pledged = pledged.Field()
    # backers = backers.Field()
    # status = status.Field()
    # description = scrapy.Field()

    # projects.xpath('//div[@class="project-cat"]/a/text()')    

    # response.xpath('//div[@id="project-list"]//div[@class="project-infobox"]')