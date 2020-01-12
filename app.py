from flask import Flask, escape, url_for, render_template, request, jsonify
import glob

# TensorFlow and tf.keras
import tensorflow as tf
#from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
import os
#from tensorflow.keras.models import Model, load_model

from skimage.io import imread, imshow, imsave
from datetime import datetime


app = Flask(__name__)

# Just disables the warning, doesn't enable AVX/FMA
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

# Model saved with Keras model.save()
MODEL_PATH = 'static/models/model_unet_checkpoint-good-2020-Jan-1.h5' 
print('Model loaded. Start serving...')  

#Load the trained model
from tensorflow import keras 
model = keras.models.load_model(MODEL_PATH) 

def predict_model(img, model):
   pred_img = model.predict(img)
   return pred_img

#Modified by naveen
@app.route('/')
def start_page():
    #create a list of dogs/cats images 
    img_list = glob.glob("static/img/*.png")[0:10]
    #img_list = [x[len("static/img/"):]  for x in img_list]
    return render_template('home3.html', img_list = img_list)


@app.route('/info')
def info():
    return 'This is the info page'

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():

   #get the image id from the request 
   payload = request.get_json() 
   print(payload) 
   print("Image id received is  " + payload["imageid"])
   
   img_path = payload["imageid"]
   #img_id = 'ade080c6618cbbb0a25680cf847f312b5e19b22bfe1cafec0436987ebe5b1e7e.png'
   img_id = img_path[len("static/img/"):]  

   #attach new time string to the predicted image file name 
   time_str = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')   

   #create the file path to store predicted image 
   pred_img_filepath = "static/pred_img/" + time_str + "_" + img_id   

   new_image = imread(img_path)[:,:,:3]  # read only three channels
   #original image szie 
   orig_shape = new_image.shape[:-1]

   #resize image to 128 to 128 
   new_image = tf.image.resize(new_image, (128, 128)) #resize the image to 128 x 128 

   image_holder = np.zeros((1, 128, 128, 3), dtype=np.uint8)  # create a list of length 1 
   image_holder[0] = new_image

   #do prediction 
   pred_img = model.predict(image_holder)

   #do thresholding and convert to uint8
   pred_img[0] = (pred_img[0] > 0.5).astype(np.uint8)  
   
   #resize predicted image to original image size    
   pred_image_upsized = tf.image.resize(pred_img[0], orig_shape)
   pred_image_upsized_sq = np.squeeze(pred_image_upsized)

   #before saving the image, delete any *.png files in the pred_folder 
   for png in glob.glob("static/pred_img/*.png"):
      os.remove(png)

   #save the predicted image and just return the filename to browser
   imsave(pred_img_filepath, pred_image_upsized_sq*255)
   #imsave(pred_img_filepath, pred_img[0])  

   return pred_img_filepath


@app.route('/load_image', methods=['POST'])
def load_image(): 
   print("In load image method in server ")
   return 'Image-Id'

with app.test_request_context():
    print(url_for('info'))