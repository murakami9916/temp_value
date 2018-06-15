# -*- coding: utf-8 -*-
import scrapy
from valu.items import Headline
"""import requests

from cachecontrol import CacheControl
import sys
"""

class ValuSpiderSpider(scrapy.Spider):
	name = 'valu_spider'
	allowed_domains = ['valu.is']
	start_urls = ('https://valu.is/users/discover',)

	"""	session = requests.session()
		cached_session = CacheControl(session)

		reponse = cached_session.get('https://valu.is/users/discover')
		print(reponse.from_cache)
		print("adakai")

		reponse = cached_session.get('https://valu.is/users/discover')
		print(reponse.from_cache)

		if not reponse.from_cache:
	"""	#print("NO UPDATE VALU")
		#sys.exit()

	def parse(self, response):
		for url in response.xpath('//div[@class="ranking_info_box"]/a/@href').extract():
			url_data = url + '/data'
			yield scrapy.Request(response.urljoin(url_data),self.parse_topics)

	def parse_topics(self, response):
		item = Headline()
		item['price'] = response.xpath('//li[@class="ag_market_value"]/em').xpath('string()').extract_first()
		item['name'] = response.xpath('//div[@class="user_introduction"]/b').xpath('string()').extract_first()
		item['job'] = response.xpath('//a[@class="tagbox"]/span').xpath('string()').extract_first()
		item['link'] = response.xpath('//ul[@class="user_nav_right"]/li/a/@href').extract_first()
		item['now'] = response.xpath('//li[@class="news_current_value"]/em').xpath('string()').extract_first()
		yield item
