from bs4 import BeautifulSoup
import requests

def get_content(url):
	r1 = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
	if r1.status_code == 403:
		raise Exception(f"Forbidden HTTP Request Error 403.\n request for: {url} \n Change request header.")

	return r1.content

def get_words(content):
	soup = BeautifulSoup(content, 'html5lib')

	content_list = []

	p_content = soup.find_all('p')
	h1_content = soup.find_all('h1')
	h2_content = soup.find_all('h2')
	h3_content = soup.find_all('h3')
	h4_content = soup.find_all('h4')
	h5_content = soup.find_all('h5')
	h6_content = soup.find_all('h6')
	span_content = soup.find_all('span')
	title_content = soup.find('title')

	content_list.append(''.join([i.get_text() for i in p_content])+" ")
	content_list.append(''.join([i.get_text() for i in h1_content])+" ")
	content_list.append(''.join([i.get_text() for i in h2_content])+" ")
	content_list.append(''.join([i.get_text() for i in h3_content])+" ")
	content_list.append(''.join([i.get_text() for i in h4_content])+" ")
	content_list.append(''.join([i.get_text() for i in h5_content])+" ")
	content_list.append(''.join([i.get_text() for i in h6_content])+" ")
	content_list.append(''.join([i.get_text() for i in span_content])+" ")
	content_list.append(title_content.get_text()+" ")

	parsed_text = ''.join(content_list)
	parsed_text_list = parsed_text.split()

	return parsed_text_list

def get_frequencies(words):
	word_freq_dict = {}

	for i in words:
		if i not in word_freq_dict:
			word_freq_dict[i] = 1
		else:
			word_freq_dict[i] += 1

	sorted_freq_dict = {}

	for i in word_freq_dict:
		max_f_word = None
		max_f = 0
		for j in word_freq_dict:
			if word_freq_dict[j] > max_f:
				max_f_word = j
				max_f = word_freq_dict[j]
		sorted_freq_dict[max_f_word] = word_freq_dict[j]
		word_freq_dict[j] = 0

	return sorted_freq_dict