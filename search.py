import sqlite3
from content_scraper import *

web_table = {}

db = sqlite3.connect('web.db')
cursor = db.cursor()

def init_db():
	cursor.execute("CREATE TABLE IF NOT EXISTS sites (url TEXT, content TEXT, keywords TEXT)")
	db.commit()

def insert_new_website(url, content):
	cursor.execute("INSERT INTO sites (url, content, keywords) VALUES (?, ?, '')", (url, content))
	db.commit()

def update_keywords(url, words):
	parsed_dict = ""
	for i in words:
		parsed_dict += i + " " + str(words[i]) + " "
	cursor.execute("UPDATE sites SET keywords=? WHERE url=?", (parsed_dict, url))
	db.commit()

def close_db():
	cursor.close()
	db.close()

init_db()

url = "https://www.crazyegg.com/blog/homepage-design/"
content = get_content(url)
words = get_words(content)
polished_words = most_common(get_frequencies(words), 75)