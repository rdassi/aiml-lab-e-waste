from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re, glob, os, cv2
import numpy as np
import pandas as pd
from shutil import copyfile
import shutil
from distutils.dir_util import copy_tree

import csv

# Flask utils
from flask import Flask, redirect, url_for, request, render_template,send_from_directory 
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
# TO RUN ON LOCAL SYSTEM
#app.config['UPLOAD_FOLDER']='/home/risha/Desktop/aiml-lab-e-waste/python-docker/uploads'

# TO RUN ON GOOGLE COLAB
app.config['UPLOAD_FOLDER']='/content/aiml-lab-e-waste/python-docker/static/uploads'
app.config['DOWNLOAD_FOLDER']='/content/aiml-lab-e-waste/python-docker'

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

        # filename = secure_filename(file.filename)
        # file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        landmark = request.form['landmark']
        pincode = request.form['pincode']

        filename_csv=pincode+".csv"
        csv_file_path="/content/aiml-lab-e-waste/python-docker/"+ filename_csv
        # This array is the fields your csv file has and in the following code
        # you'll see how it will be used. Change it to your actual csv's fields.
        
        # GET RESULTS FROM OBJECT DETECTION
        # {"battery":1,"bulb":1,"keyboard":1,"laptop":0,"mobile phone":0,"monitor":0,"mouse":0,"phone":0}
      
        #result_label= detect.detect(weights='/home/risha/Desktop/aiml-lab-e-waste/python-docker/weights/best.pt', source=file_path, view_img=True,project='/home/risha/Desktop/aiml-lab-e-waste/python-docker/runs/detect', save_txt=True)

        # TO RUN ON COLAB
        result_label= detect.detect(weights='/content/aiml-lab-e-waste/python-docker/weights/best.pt', save_txt=True, project='/content/aiml-lab-e-waste/python-docker/static/runs', view_img=True, source=file_path)

        #FIELDS STORED IN CSV FILE
        fieldnames = ['name', 'email','phone','landmark','pincode','battery', 'bulb', 'keyboard', 'laptop', 'mobile phone', 'monitor', 'mouse']
        #if os.path.exists(file_path):
        #df = pd.read_csv(filename_csv) # or pd.read_excel(filename) for xls file
        # We repeat the same step as the reading, but with "w" to indicate
        # the file is going to be written.
        with open(filename_csv,'a+') as inFile:
            # DictWriter will help you write the file easily by treating the
            # csv as a python's class and will allow you to work with
            # dictionaries instead of having to add the csv manually.
            writer = csv.DictWriter(inFile, fieldnames=fieldnames)
            #writer.writeheader()
            #csv_dict = [row for row in csv.DictReader(csvfile)]
            #csv_dict = [row for row in csv.DictReader(inFile)]
            
            #if df.empty is True:
            if os.stat(csv_file_path).st_size == 0:
              writer.writeheader()
              #writer.writerow({'name': 'Name', 'email': 'Email', 'phone':'Phone','landmark':'Landmark', 'pincode':'Pincode','battery': 'battery', 'bulb': 'bulb', 'keyboard': 'keyboard', 'laptop':'laptop', 'mobile phone': 'mobile phone', 'monitor': 'monitor', 'mouse': 'mouse' })

            # writerow() will write a row in your csv file
            # {"battery":1,"bulb":1,"keyboard":1,"laptop":0,"mobile phone":0,"monitor":0,"mouse":0,"phone":0}
            writer.writerow({'name': name, 'email': email, 'phone':phone,'landmark':landmark, 'pincode':pincode,'battery': result_label['battery'], 'bulb': result_label['bulb'], 'keyboard': result_label['keyboard'], 'laptop': result_label['laptop'], 'mobile phone': result_label['mobile phone'], 'monitor': result_label['monitor'], 'mouse': result_label['mouse'] })

        # Make prediction
        #similar_glass_details=glass_detection.getUrl(file_path)
        
        #return jsonify(res)
        # /home/risha/Desktop/aiml-lab-e-waste/python-docker/uploads
    #ON SYSTEM
    # return render_template('result.html', img_path=f"/home/risha/Desktop/aiml-lab-e-waste/python-docker/uploads/{filename}",detected_img_path=f"/content/aiml-lab-e-waste/python-docker/runs/detect/{filename}",battery=result_label['battery'],  bulb= result_label['bulb'], keyboard=result_label['keyboard'], laptop= result_label['laptop'], mobile_phone=result_label['mobile phone'], monitor=result_label['monitor'], mouse=result_label['mouse'])

    #img_path= "/content/aiml-lab-e-waste/python-docker/uploads/" + str(filename)
    img_path= "./static/uploads/" + str(filename)
    detected_img_path= "./static/runs/detect/" + str(filename)
    # ON COLAB
    return render_template('result.html', img_path=img_path,detected_img_path=detected_img_path,battery=result_label['battery'],  bulb= result_label['bulb'], keyboard=result_label['keyboard'], laptop= result_label['laptop'], mobile_phone=result_label['mobile phone'], monitor=result_label['monitor'], mouse=result_label['mouse'])

@app.route('/getpincodedeets', methods=['POST'])
def ugetpincodedeets():
# @app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
# def download(filename):
    print(request.form['pincode'])
    collector_pincode=request.form['pincode']
    # Appending app path to upload folder path within app root folder
    filename_collector=collector_pincode+ ".csv"

    # CHANGE PATH AS PER YOUR LOCAL SYSTEM
    #uploads = os.path.join('/home/Desktop/aiml-lab-e-waste/python-docker', filename_collector)

    # TO RUN ON COLAB
    uploads = os.path.join('/content/aiml-lab-e-waste/python-docker', filename_collector)
    # Returning file from appended path
    if os.path.exists(uploads):
      return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename_collector, as_attachment=True)
    else:
      return "No e-waste in this area"
    #return send_from_directory(directory=uploads, path=filename_collector, as_attachment=True)
if __name__ == '__main__':
    app.run()
    
