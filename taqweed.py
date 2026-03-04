from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/')
def index():
	return render_template('main.html')


@app.route('/second')
def second():
    return render_template('second.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/what-is-tajweed')
def what_is_tajweed():
    return render_template('what-is-tajweed.html')

@app.route('/history-of-tajweed')
def history_of_tajweed():
    return render_template('history-of-tajweed.html')

@app.route('/tajweed-rules')
def tajweed_rules():
    return render_template('tajweed-rules.html')
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000) 

