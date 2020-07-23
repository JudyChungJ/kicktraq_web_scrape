from scrapy import Spider, Request
from kicktraq.items import KicktraqItem
import re

class KicktraqSpider(Spider):
    name = 'kicktraq_spider'
    allowed_urls = ['https://www.kicktraq.com']
    start_urls = ['https://www.kicktraq.com/archive/?page=1']
    

    def parse(self, response):
        projects = response.xpath('//div[@class="project-infobox"]') # goes to infobox that contains h2 project-cat and project-infobits

        for project in projects:
            names = project.xpath('./h2/a/text()').extract_first() # in h2
            print('='*50)
            print(">>> name in for loop:", names)
            print('='*50)
            
            category = project.xpath('./div[@class="project-cat"]/a/@href').extract() #project-cat href as string
            main_category = ''
            if len(category) == 1:
                main_category = category[0].strip('/').replace('categories/','')
                category = None
            else:
                main_category = category[0].strip('/').replace('categories/','')
                category = category[1].strip('/').replace('categories/','').replace('/','|')
            
            money = project.xpath('.//div[@class="project-details"]/text()[2]').extract_first()
            currency, pledged, goal = [s.replace(',', '') for s in [str(el) for el in re.findall(' (.)(.*) of .(.*) ' , money)[0]]]
            goal = int(goal)
            pledged = int(pledged)

            # dates = project.xpath('.//div[@class="project-details"]/text()').extract()   
            # year = re.findall('\((\d*)\)', dates)[0]
            # start_month, start_day = [el for el in re.findall('Dates: (\D*) (\d*)..', dates)[0]]
            # start_date = '-'.join([year, start_month, start_day])

            # end_month, end_day = [el for el in re.findall(' -> (\D*) (\d*)', dates)[0]]
            # deadline = '-'.join([year, end_month, end_day])

            backers = project.xpath('.//div[@class="project-details"]/text()[1]').extract_first()
            backers = int(re.findall('Backers: (\d*)', backers)[0])

            status = project.xpath('.//div[@class="project-pledgilizer"]//h5/text()').extract_first()

            description = project.xpath('./div[1]/text()').extract_first()




            
#"|".join(category.strip('/').replace('categories/','').split('/'))







            item = KicktraqItem()
            item['names'] = names
            item['category'] = category
            item['main_category'] = main_category
            item['currency'] = currency
            item['goal'] = goal
            item['pledged'] = pledged
            # item['start_date'] = start_date
            # item['deadline'] = deadline
            item['backers'] = backers
            item['status'] = status
            item['description'] = description
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