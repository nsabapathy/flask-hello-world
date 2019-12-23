from flask import Flask, escape, url_for
app = Flask(__name__)

#Modified by naveen
@app.route('/')
def hello_world():
    return 'This is test of Render service!'


@app.route('/info')
def info():
    return ' This is the info page'

with app.test_request_context():
    print(url_for('info'))