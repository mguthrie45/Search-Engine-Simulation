import sqlite3
from content_scraper import *

def init_db(db, cursor):
	cursor.execute("CREATE TABLE IF NOT EXISTS sites (url TEXT, content TEXT, keywords TEXT)")
	db.commit()

def insert_new_website(db, cursor, url, content):
	cursor.execute("INSERT INTO sites (url, content, keywords) VALUES (?, ?, '')", (url, content))
	db.commit()

def update_keywords(db, cursor, url, words):
	parsed_dict = ""
	for i in words:
		parsed_dict += i + " " + str(words[i]) + " "
	parsed_dict = parsed_dict[:len(parsed_dict)-1]
	cursor.execute("UPDATE sites SET keywords=? WHERE url=?", (parsed_dict, url))
	db.commit()

def add_row(db, cursor, url):
	content = get_content(url)
	words = get_words(content)
	polished_words = most_common(get_frequencies(words), 75)

	insert_new_website(db, cursor, url, content)
	update_keywords(db, cursor, url, polished_words)


def split_keyword_string(keywords):
	keyword_list = keywords.split()
	keyword_dict = {}
	for i in range(len(keyword_list)-1):
		if i % 2 == 0:
			word = keyword_list[i]
			freq = int(keyword_list[i+1])
			keyword_dict[word] = freq

	return keyword_dict

def get_keywords(cursor, url):
	cursor.execute("SELECT keywords FROM sites WHERE url=?", (url,))
	keywords, = cursor.fetchall()[0]

	keyword_dict = split_keyword_string(keywords)

	return keyword_dict

def append_upper_variant(word_list):
	return word_list + [i[0].upper()+i[1:len(i)] for i in word_list]

def get_keyword_relations(cursor, search_words):
	keyword_relations = {}
	search_words = append_upper_variant(search_words)

	cursor.execute("SELECT url, keywords FROM sites")
	fetched = cursor.fetchall()

	for i in fetched:
		url, keywords = i

		keyword_dict = split_keyword_string(keywords)

		freq_dict = {}
		for j in keyword_dict:
			if j in search_words:
				freq_dict[j] = keyword_dict[j]
		keyword_relations[url] = freq_dict

	return keyword_relations            #{url: {word1: f1, word2: f2}}

def get_weightings(keyword_relations):
	weightings = {}
	max_total_freq = 0
	for url in keyword_relations:
		total_freq = 0
		words = keyword_relations[url]
		for word in words:
			total_freq += words[word]
		if total_freq > max_total_freq:
			max_total_freq = total_freq
		weightings[url] = total_freq

	return weightings

def n_most_relevant(cursor, n, search_words):
	keyword_relations = get_keyword_relations(cursor, search_words)
	weightings = get_weightings(keyword_relations)

	sorted_weightings = {url: weight for url, weight in sorted(weightings.items(), key=lambda item: item[1], reverse=True)[:n]}

	return sorted_weightings

def close_db():
	cursor.close()
	db.close()

def add_urls(db, cursor, url_list):
	for url in url_list:
		add_row(db, cursor, url)

