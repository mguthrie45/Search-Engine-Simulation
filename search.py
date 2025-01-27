import sqlite3
from content_scraper import *

def init_db(db, cursor):
	cursor.execute("CREATE TABLE IF NOT EXISTS sites (url TEXT, title TEXT, content TEXT, keywords TEXT, UNIQUE(url))")
	db.commit()


def insert_new_website(db, cursor, url, title, content):
	cursor.execute("INSERT INTO sites (url, title, content, keywords) VALUES (?, ?, ?, '')", (url, title, content))
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
	title = get_title(url)
	polished_words = most_common(get_frequencies(words), 75)

	if content == 'Connection refused.':
		return None
	insert_new_website(db, cursor, url, title, content)
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


def get_title_from_db(cursor, url):
	cursor.execute("SELECT title FROM sites WHERE url=?", (url,))
	title, = cursor.fetchall()[0]

	return title


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

	db = sqlite3.connect('web.db')
	cursor = db.cursor()

	sorted_list = sorted(weightings.items(), key=lambda item: item[1], reverse=True)
	if len(sorted_list) >= n:
		sorted_list = sorted_list[:n]
	sorted_weightings = {url: weight for url, weight in sorted_list}

	cleaned_sorted_weightings = {}
	for i in sorted_weightings:
		title_descr_i = get_title_from_db(cursor, i)+get_meta_descr(i)
		title_descrs = list(map(lambda x: get_title_from_db(cursor, x)+get_meta_descr(x), cleaned_sorted_weightings))
		if title_descr_i not in title_descrs:
			cleaned_sorted_weightings[i] = sorted_weightings.get(i)
	print(cleaned_sorted_weightings)
	return cleaned_sorted_weightings


def close_db():
	cursor.close()
	db.close()


def add_urls(db, cursor, url_list):
	for url in url_list:
		add_row(db, cursor, url)

		

url_list = ["https://www.crazyegg.com/blog/homepage-design/",
	"https://www.cnn.com/",
	"https://www.foxnews.com/",
	"https://sallysbakingaddiction.com/homemade-pizza-crust-recipe/",
	"https://www.foodrepublic.com/recipes/all-american-cheeseburger-recipe/",
	"https://butterwithasideofbread.com/easy-cheeseburger-recipe/",
	"https://www.codecademy.com/learn/paths/computer-science?g_network=g&g_productchannel=&g_adid=434619800290&g_locinterest=&g_keyword=learn%20to%20program&g_acctid=243-039-7011&g_adtype=search&g_adtype=&g_keywordid=kwd-11352741&g_campaign=US+Career+Path%3A+Pro+-+Exact&g_ifcreative=&g_campaign=account&g_locphysical=1025354&g_adgroupid=102526214618&g_productid=&g_source={sourceid}&g_merchantid=&g_placement=&g_partition=&g_campaignid=10030170706&g_ifproduct=&utm_id=t_kwd-11352741:ag_102526214618:cp_10030170706:n_g:d_c&utm_term=learn%20to%20program&utm_campaign=US%20Career%20Path%3A%20Pro%20-%20Exact&utm_source=google&utm_medium=paid-search&utm_content=434619800290&hsa_acc=2430397011&hsa_cam=10030170706&hsa_grp=102526214618&hsa_ad=434619800290&hsa_src=g&hsa_tgt=kwd-11352741&hsa_kw=learn%20to%20program&hsa_mt=e&hsa_net=adwords&hsa_ver=3&gclid=CjwKCAjwoc_8BRAcEiwAzJevtW6BoXSub_GZa_grl_HsqX3nBfhXn7dsC-Mu-EP8bDTNdAz8rMovYxoCfPQQAvD_BwE"
]

