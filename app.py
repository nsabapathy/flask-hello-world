from flask import Flask, escape, url_for, render_template


app = Flask(__name__)

#Modified by naveen
@app.route('/')
def hello_world():
    return render_template('home3.html', message='This is a hello')


@app.route('/info')
def info():
    return ' This is the info page'

with app.test_request_context():
    print(url_for('info'))