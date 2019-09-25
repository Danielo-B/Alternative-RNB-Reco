#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 15:22:27 2019

@author: danielobennett
"""

'''
Import libraries
'''

from flask import Flask, render_template, url_for, request, redirect, flash
from gensim.models.doc2vec import Doc2Vec

import pandas as pd
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
#for securing files before upload
from werkzeug.utils import secure_filename

#audio data stuff
import librosa 
import librosa.display

from keras.applications import VGG16
from keras.models import Model
import cv2
from scipy.spatial.distance import cosine
from keras.models import load_model
import tensorflow as tf


'''
Start to define helper functions
'''


##ORDER 1: make sure the artist and song are in the model
def check_inputs(artist_name, song_name):
    """
    Ensures that the inputted artist names and songs exist in the model 
    ???? Will use with a list of songs/artists pkl or generate from model 
    ???? Should separate since will have 2 inputs?
    """
    if artist_name not in artist_list or song_name not in song_list:
        return redirect(request.url)

#ORDER 2: combine inputs to make ready for model input 
def combine_inputs(artist_name, song_name):
    """
    Combines the 2 inputs so that can pipe them in the model
    NOTE: Does title so that it should work but not sure what to do since songs and artists are not such 
    #Change model so that it can search properly????
    """
    return (artist_name + '|' + song_name) #.title() #should be lower as input to model


#ORDER 3: return clean info from model
def show_results_clean(samp_tup):
    """
    Extract just the artist and name from the results tuple
    input is a list of tuples 
    invoke within a for loop
    """
    #return samp_tup[0].split("|", 1)[0], samp_tup[0].split("|", 1)[1]
    #print("\nYou might like", samp_tup[0].split("|", 1)[1], "by", samp_tup[0].split("|", 1)[0])
    return str("You might like "+ samp_tup[0].split("|", 1)[1]+ " by "+ samp_tup[0].split("|", 1)[0])

    
#audio Functions
def extract_vector(new_path):
    y, sr = librosa.load(new_path, offset=20, duration=30)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)#,fmax=8000
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.power_to_db(S ,ref=np.max))
    plt.tight_layout()
    temp_path = new_path.split('/')[1]
    file_pref = temp_path.split('.mp3')[0]
    output_f = "../test_songs/" + file_pref + ".png"  #save in appropriate folder 
    plt.savefig(output_f, transparent=True, pad_inches=0.0)
    plt.close()
        #save the file and open with opencv######## 
    img = cv2.imread(output_f) #no need to read in 
    img = cv2.resize(img,(224,224))
    img = np.reshape(img,[1,224,224,3])
    with graph.as_default():
        img_vector = feature_extractor.predict(img)
    #img_vector = feature_extractor.predict(img)
    img_vector  = img_vector.tolist()[0] # should give regular python list
    return img_vector   

#calculate cosign distance
def cosine_similarity(row, recommendation_vector):
    distance = cosine(row["vectors"], recommendation_vector)
    return distance
    
#get recos from model 
def plot_recommendations(new_path, recommendation_name):
    rec_vector = extract_vector(new_path)
    df[recommendation_name] = df.apply(cosine_similarity, axis=1, recommendation_vector = rec_vector)
    top_recommendations = df.sort_values(recommendation_name, ascending=False)#.head(10)
    return top_recommendations
    
'''
ACTUAL FLASK CODE
'''

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/danielobennett/metis/work/projects/Project05/test_songs/'
app.secret_key = 'some secret key'

with open('../flask_df.pkl', 'rb') as picklefile:
    df= pickle.load(picklefile)
feature_extractor = load_model('../model_predict.h5')
graph = tf.get_default_graph()


#homepage
@app.route('/')
def home():
	return render_template('home.html')

#for redirecting purposes
@app.route('/')
def home_link():
	redirect(url_for('home'))
    
#lyrical reco page
@app.route('/lyrical')
def lyrical():
	return render_template('lyrical.html')

#for redirecting purposes
@app.route('/lyrical', methods=['GET', 'POST'])
def lyrical_link():
	return redirect(url_for('lyrical'))

#results of lytrical recommendation page
@app.route('/lyrical_results', methods=['GET', 'POST']) #is post since we're retreiving...
def recommend():
    if request.method == 'POST':
        artist_name = request.form['artist_name']
        song_name = request.form['song_name'] 
        #check_inputs(artist_name, song_name) #verify inputs > NEED LISTS TO CHECK 
        input_string = combine_inputs(artist_name, song_name) #combine as input 
        
        model = Doc2Vec.load('../alt_rnb_lyrics.doc2vec')
        results = model.docvecs.most_similar([model.docvecs[input_string]], topn=6) #make a variable?
        
        start_message = "Since you liked " +  artist_name + "'s " +  song_name +  ", give these songs a try!\n"  #reverifies input
        app_results = [] #collect all strings
        for item in results:    
            temp_line = show_results_clean(item)
            if song_name in temp_line: #skips if it is hte same as the input song
                continue
            app_results.append(temp_line) # append strings to list > iter in html
        return render_template('lyrical_results.html', start_message = start_message, reco_results = app_results)


#audio reco page
@app.route('/audio')
def audio():
	return render_template('audio.html')

#for redirecting purposes
@app.route('/audio', methods=['GET', 'POST'])
def audio_link():
	return redirect(url_for('audio'))


#audio recommendation results
@app.route('/audio_results', methods=["POST", "GET"])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if "myFile" not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files["myFile"]
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filename = "/Users/danielobennett/metis/work/projects/Project05/test_songs/Sasha_Keable-Treat_Me_Like_I'm_All_Yours.mp3"
        df = pd.read_csv("../song_vectors.csv")
        feature_extractor = load_model('../model_predict.h5')
        recs = plot_recommendations(filename, recommendation_name = "recommendation")
        var = recs.iloc[0]['song']
        var = str(var.replace("_", " ")).split('.png')[0].strip()
        artist = var.split('-')[0].strip()
        song = var.split('-')[1].strip().title()
        start_message = "Based on the song you uploaded, you should give the following song a listen to: "
        #print("You would like", var.split('-')[1].strip().title(),"by", var.split('-')[0].strip())
        message = str(song+ " by "+ artist)
        
        return render_template('audio_results.html',
                               response = message, 
                               intro_portion = start_message)


if __name__ == '__main__':
	app.run(debug=False)
#	app.run(debug=True)
