import urlparse

import scrapy

from ninegag.items import NineGag, Joke


class NGagSpyder(scrapy.Spider):
    name = "9gagspy"
    allowed_domains = ["9gag.com"]
    start_urls = ["http://9gag.com"]

    COUNT_MAX = 30
    count = 0

    def parse_read_more(self, response):
        gag_item = NineGag()
        gag_source_url = response.css('.badge-post-container').xpath('a/img/@src').extract_first()
        gag_title = response.xpath('//article/header/h2/text()').extract_first()
        gag_item['title'] = gag_title
        gag_item['source_url'] = [gag_source_url]
        return gag_item



    def parse(self, response):
        gag_articles = response.xpath(
            '//*[@class="badge-entry-collection"]//article')
        for gag in gag_articles:
            gag_item = NineGag()
            gag_content = gag.extract()
            gag_title = gag.xpath('header/h2/a/text()').extract_first()
            gag_title = gag_title.strip(" \n")
            gag_id = gag.xpath('@data-entry-id').extract_first()
            gag_item['title'] = gag_title
            gag_points = gag.xpath('p[@class="post-meta"]').xpath('a/span/text()').extract_first()
            gag_points = int(gag_points.replace(',', ''))
            gag_item['points'] = gag_points
            read_more_post = gag.css('.badge-post-container').css('.post-read-more').xpath('text()').extract_first()
            if read_more_post == u'View Full Post ':
                read_whole_post_url = gag.css('.badge-post-container').css('.post-read-more').xpath('@href').extract_first()
                yield scrapy.Request(urlparse.urljoin(response.url, read_whole_post_url), callback=self.parse_read_more)
                continue

            gag_source_url = gag.css('.badge-post-container').xpath('a/img/@src').extract_first()
            if gag_source_url is None:
                gag_source_url = gag.css('.badge-post-container').xpath('a').\
                    css('.badge-animated-container-animated').xpath('video/source/@src').extract_first()
                gag_item['is_video'] = True
            if gag_source_url is None:
                continue
            gag_item['source_url'] = [gag_source_url]
            self.count = self.count + 1
            yield gag_item

        if (self.count < self.COUNT_MAX):
            next_url = 'http://9gag.com/?id=%s&c=10' % gag_id
            print next_url
            yield scrapy.Request(next_url, callback=self.parse)

priority_nr = 100

class JokesSpyder(scrapy.spiders.Spider):
    name = "jokesspy"
    allowed_domains = ["laughfactory.com"]
    start_urls = ["http://www.laughfactory.com/jokes"]


    def parse(self, response):
        global priority_nr
        category_links = response.xpath('//div[@class="left-nav"]/ul').xpath(
            './/li/a/@href').extract()

        for link in category_links:
            yield scrapy.Request(link, callback=self.parse_page, priority=priority_nr)
            priority_nr -= 1

    def parse_page(self, response):
        global priority_nr
        jokes_div = response.xpath('//*[@class="joke-area"]')
        for joke in jokes_div.xpath('.//*[@class="line"]'):
            joke_id = joke.xpath('.//p/@id').extract_first()
            joke_text = joke.xpath('.//p/text()').extract()
            joke_text = ' '.join(joke_text)
            # joke_text = joke_text.strip(" \n")
            joke_text = " ".join(joke_text.split())
            joke_likes = joke.xpath('.//div[@class="thum-like-number"]/text()').extract_first()
            joke_dislikes = joke.xpath('.//div[@class="thum-dislike-number"]/text()').extract_first()
            joke_category = response.xpath('//div[@class="new-content"]').xpath('.//span[@class="relation-color"]/text()').extract_first()
            joke_category = " ".join(joke_category.split())
            joke_item = Joke()
            joke_item['text'] = joke_text
            joke_item['likes'] = int(joke_likes)
            joke_item['dislikes'] = int(joke_dislikes)
            joke_item['category'] = joke_category
            joke_item['identifier'] = joke_id + joke_category
            yield joke_item


        next_page = jokes_div.xpath('.//div[@class="pagination"]//li//span//a')[-1].extract()
        next_page_nr = int(jokes_div.xpath('.//div[@class="pagination"]//li//span//a/@href')[-1].extract()[-1])
        if "list-next" in next_page and next_page_nr <= 2:
            next_page = jokes_div.xpath('.//div[@class="pagination"]//li//span/a/@href')[ -1].extract()
            yield scrapy.Request(next_page, callback=self.parse_page, dont_filter=False, priority=priority_nr)
            priority_nr -= 1


from scrapy.crawler import Crawler
from scrapy import signals
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings

class UrlCrawlerScript(Process):
        def __init__(self, spider):
            Process.__init__(self)
            settings = get_project_settings()
            self.crawler = Crawler(settings)
            self.crawler.configure()
            self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
            self.spider = spider

        def run(self):
            self.crawler.crawl(self.spider)
            self.crawler.start()
            reactor.run()

def run_spider():
    spider = NGagSpyder()
    crawler = UrlCrawlerScript(spider)
    crawler.start()
    crawler.join()