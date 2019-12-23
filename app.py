from flask import Flask
app = Flask(__name__)

#Modified by naveen
@app.route('/')
def hello_world():
    return 'This is test of Render service!'
