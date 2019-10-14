from scrapy import Spider
from scrapy import Request
from webmd.items import WebmdItem
import re

class WebMDSpider(Spider):
    name = 'webmd_comment_spider'
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
        supplement = response.xpath('//div[@class="tb_main"]/h1/text()').extract_first()[25:]

        conditionInfo = response.xpath('//*[@id="ratings_fmt"]/div/div[1]/div[1]/text()').extract()
        for i in range(len(conditionInfo)):
            div_num = str(5 + i)
            
            commentField = response.xpath('//*[@id="comFull' + str(i + 1) + '"]/text()').extract()
            if (commentField == []):
                comment = ''
            else:
                comment = commentField[0]
            dateTime = response.xpath('//*[@id="ratings_fmt"]/div[' + str(i + 5) + ']/div[1]/div[2]/text()').extract_first()
            
            item = WebmdItem()
            item['dateTime'] = dateTime
            item['conditionInfo'] = conditionInfo
            item['supplement'] = supplement
            item['comment'] = comment
            yield item