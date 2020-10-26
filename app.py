from flask import Flask, render_template, request
import search

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html', urls=[])

@app.route('/search', methods=['GET', 'POST'])
def search():
	search_input = request.form.get('search', False)

	if search_input != False:
		print(search_input)
		search_words = search_input.split()
		urls = search.n_most_relevant(3, search_words)
		return render_template('index.html', urls=urls)
	return redirect(url_for('main'))

if __name__ == '__main__':
	app.run(debug=True)