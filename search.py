import sqlite3
from content_scraper import *

web_table = {}

db = sqlite3.connect('web.db')
cursor = db.cursor()

def init_db():
	cursor.execute("CREATE TABLE IF NOT EXISTS sites (url text, content text)")
	db.commit()

def insert_data(url, content):
	cursor.execute("INSERT INTO sites (url, content) VALUES (?, ?)", (url, content))
	db.commit()
	cursor.close()
	db.close()

init_db()

url = "https://www.crazyegg.com/blog/homepage-design/"
content = get_content(url)
words = get_words(content)
print(get_frequencies(words))