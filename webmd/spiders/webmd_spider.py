from scrapy import Spider
from scrapy import Request
from webmd.items import WebmdItem
import re

class WebMDSpider(Spider):
    name = 'webmd_spider'
    allowed_urls = ['https://www.webmd.com/']
    start_urls = ['https://www.webmd.com/vitamins/index']


    def parse(self, response):
        results_urls = response.xpath('//div[@class="vitamins-common-results"]//a[2]/@href').extract()
            #return a list of links for common vitamins and supplement
        
        #checkpoint
        # print('='*50)
        # print(len(results_urls))
        # print('='*50)
        add_filter = '&sortby=3&conditionFilter=-1'

        for url in results_urls: #needt to remove 2 after testing
            url = url+add_filter
            yield Request(url=url, callback=self.parse_result_page, meta={'url':url})


    def parse_result_page(self, response):
        url = response.meta['url']
        #need to get how many pages of review
        # Now identify how many review pages to be scraped per supplement
        # pages is first page, following three lines determine how many "next pages"
        text = response.xpath('//div[@class="postPaging"]/text()').extract_first()
        _, per_page, total_reviews = map(lambda x: int(x), re.findall('\d+',text))
        num_pages = total_reviews // per_page

        root_url = re.sub('&sortby=3&conditionFilter=-1','', url)

        for url in [root_url+'&pageIndex={}&sortby=3&conditionFilter=-1'.format(i) for i in range(num_pages+1)]: #fixed 2 to num_pages+1
            #checkpoint
            # print('='*50)
            # print(url)
            # print('='*50)
            yield Request(url=url, callback=self.parse_reviews_scrape)


    def parse_reviews_scrape(self, response):
        first_review_page = response.xpath('//div[@class="userPost"]').extract_first()
        reviews = response.xpath('//div[@class="userPost"]')

        # SECOND CHECKPOINT
        # print('='*50)
        # print(len(reviews))
        # print('='*50)

        #extracting review data from reviews
        for review in reviews: #need to remove 2
            supplement = response.xpath('//div[@class="tb_main"]/h1/text()').extract_first()[25:]
            conditionInfo = review.xpath('//span[@class="reason"]/text()').extract_first() 
            dateTime = review.xpath('.//div[@class="date"]/text()').extract_first()
            reviewerInfo = review.xpath('.//p[@class="reviewerInfo"]/text()').extract_first()[9:].strip()
            effectiveness = int(review.xpath('.//span[@class="current-rating"]/text()').extract()[0].strip()[16:])
            easeOfUse = int(review.xpath('.//span[@class="current-rating"]/text()').extract()[1].strip()[16:])
            satisfaction = int(review.xpath('.//span[@class="current-rating"]/text()').extract()[2].strip()[16:])
            comment = review.xpath('//p[@class="comment"]/text()').extract_first()
            helpful = int(review.xpath('//p[@class="helpful"]/text()').extract_first()[:3].strip())


        # create review item
            item = WebmdItem()
            item['supplement'] = supplement
            item['conditionInfo'] = conditionInfo
            item['dateTime'] = dateTime
            item['reviewerInfo'] = reviewerInfo
            item['effectiveness'] = effectiveness
            item['easeOfUse'] = easeOfUse
            item['satisfaction'] = satisfaction
            item['comment'] = comment
            item['helpful'] = helpful
            yield item


