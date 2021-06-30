from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re, glob, os,cv2
import numpy as np
import pandas as pd
from shutil import copyfile
import shutil
from distutils.dir_util import copy_tree

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

import detect

# Define a flask app
app = Flask(__name__)

#for f in os.listdir("static\\similar_images\\"):
#    os.remove("static\\similar_images\\"+f)

#print('Model loaded. Check http://127.0.0.1:5000/')
from flask_ngrok import run_with_ngrok
from flask import Flask

app=Flask(__name__)
run_with_ngrok(app)
app.config['UPLOAD_FOLDER']='/home/risha/Desktop/aiml-lab-e-waste/python-docker/uploads'
@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    # if request.method == 'POST':
    #     # Get the file from post request
    #     f = request.files['file']

    #     # Save the file to ./uploads
    #     basepath = os.path.dirname(__file__)
    #     file_path = os.path.join(
    #         basepath, 'uploads', secure_filename(f.filename))
    #     f.save(file_path)
    #     flash(file_path)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Make prediction
        #similar_glass_details=glass_detection.getUrl(file_path)
        return detect.detect(weights='/home/risha/Desktop/aiml-lab-e-waste/python-docker/weights/best.pt', source=file_path, view_img=True,project='/home/risha/Desktop/aiml-lab-e-waste/python-docker/runs/detect', save_txt=True)
        #return jsonify(res)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
    