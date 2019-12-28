from flask import Flask, escape, url_for, render_template
import glob

app = Flask(__name__)

#Modified by naveen
@app.route('/')
def hello_world():
    #create a list of dogs/cats images 
    print("In hello world")
    img_list = glob.glob("static/img/*.jpg")[0:10]
    print(img_list)
    return render_template('home3.html', img_list = img_list)


@app.route('/info')
def info():
    return 'This is the info page'

@app.route('/analyze', methods=['POST'])
def analyze():
   return 'From Analyze function'


@app.route('/load_image', methods=['POST'])
def load_image(): 
   print("In load image method in server ")
   return 'Image-Id'

with app.test_request_context():
    print(url_for('info'))