from flask import Flask, render_template, request
import search as Searcher
import content_scraper as Scraper
import sqlite3

url_list = ["https://www.crazyegg.com/blog/homepage-design/",
	"https://www.cnn.com/",
	"https://www.foxnews.com/",
	"https://sallysbakingaddiction.com/homemade-pizza-crust-recipe/",
	"https://www.foodrepublic.com/recipes/all-american-cheeseburger-recipe/",
	"https://butterwithasideofbread.com/easy-cheeseburger-recipe/",
	"https://www.codecademy.com/learn/paths/computer-science?g_network=g&g_productchannel=&g_adid=434619800290&g_locinterest=&g_keyword=learn%20to%20program&g_acctid=243-039-7011&g_adtype=search&g_adtype=&g_keywordid=kwd-11352741&g_campaign=US+Career+Path%3A+Pro+-+Exact&g_ifcreative=&g_campaign=account&g_locphysical=1025354&g_adgroupid=102526214618&g_productid=&g_source={sourceid}&g_merchantid=&g_placement=&g_partition=&g_campaignid=10030170706&g_ifproduct=&utm_id=t_kwd-11352741:ag_102526214618:cp_10030170706:n_g:d_c&utm_term=learn%20to%20program&utm_campaign=US%20Career%20Path%3A%20Pro%20-%20Exact&utm_source=google&utm_medium=paid-search&utm_content=434619800290&hsa_acc=2430397011&hsa_cam=10030170706&hsa_grp=102526214618&hsa_ad=434619800290&hsa_src=g&hsa_tgt=kwd-11352741&hsa_kw=learn%20to%20program&hsa_mt=e&hsa_net=adwords&hsa_ver=3&gclid=CjwKCAjwoc_8BRAcEiwAzJevtW6BoXSub_GZa_grl_HsqX3nBfhXn7dsC-Mu-EP8bDTNdAz8rMovYxoCfPQQAvD_BwE"
]

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html', info=[])

@app.route('/search', methods=['GET', 'POST'])
def search():
	db = sqlite3.connect('web.db')
	cursor = db.cursor()

	search_input = request.form.get('search', False)

	if search_input != False:
		print(search_input)
		search_words = search_input.split()
		urls = list(Searcher.n_most_relevant(cursor, 3, search_words))
		print(urls)
		titles = [Searcher.get_title_from_db(cursor, url) for url in urls]
		descrs = [Scraper.get_meta_descr(url) for url in urls]

		info = [(urls[i], titles[i], descrs[i]) for i in range(len(urls))]

		return render_template('index.html', info=info)
	return redirect(url_for('main'))

if __name__ == '__main__':
	app.run(debug=True)