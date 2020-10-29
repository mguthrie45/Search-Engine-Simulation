import content_scraper as Scraper 
import search as Searcher
import sqlite3
import random

import threading






'''TODO:
Account for paths within the website files i.e. ones without 'https://'
'''





class God:
	def __init__(self):
		self.crawlbot_book = []

	def birth_crawler(self):
		c = Crawler(self, is_beginner=True)
		self.crawlbot_book.append(c)

	def move_crawlers(self):
		for i in self.crawlbot_book:
			if i.urls_to_visit and len(i.urls_to_visit) > 0:
				dest_url = random.choice(i.urls_to_visit)
				print(dest_url)
				i.jump_to_url(dest_url)
			else:
				print('empty')


	def life_sweep(self, replacement_number):
		for crawler in self.crawlbot_book:
			if crawler.age > 10:
				crawler.die()
				self.birth_crawler()
		if self.crawlbot_book == []:
			for i in range(replacement_number):
				self.birth_crawler()

class Crawler:
	def __init__(self, god, is_beginner=False, start_url=None):
		self.is_beginner = is_beginner
		if self.is_beginner:
			self.current_url = self.get_start_url()
		else:
			self.current_url = start_url
		self.god = god
		self.urls_to_visit = self.find_new_urls()
		self.age = 0

	def get_start_url(self):
		db = sqlite3.connect('web.db')
		cursor = db.cursor()

		cursor.execute("SELECT url FROM sites ORDER BY RANDOM() LIMIT 1")
		url, = cursor.fetchall()[0]
		return url

	def save_current_url(self):
		db = sqlite3.connect('web.db')
		cursor = db.cursor()

		Searcher.add_row(db, cursor, self.current_url)

	def find_new_urls(self):
		url_list = Scraper.get_a_tags(self.current_url)
		return url_list

	def birth_crawler(self, start_url):
		c = Crawler(start_url=start_url)
		self.god.crawlbot_book.append(c)

	def jump_to_url(self, url):
		self.current_url = url
		self.save_current_url()
		self.age += 1

	def die(self):
		del self


if __name__ == '__main__':
	god = God()
	god.life_sweep(10)

