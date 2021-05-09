# -*- coding: utf-8 -*-
"""
Created on Sat May  8 15:34:22 2021

@author: akanksha_pandey
"""

import pygame
import tkinter as tk
from tkinter import *  # not advisable to import everything with *
from tkinter import filedialog
import tkinter.font as tkFont
from PIL import Image, ImageTk
import os
import numpy as np
import pandas as pd
from scipy import spatial
import librosa
import librosa.display
import statistics
from statistics import *
from sklearn.neighbors import NearestNeighbors

import pandas as pd
data = pd.read_csv('finaldataset.csv')
data.drop('Unnamed: 0',
  axis='columns', inplace=True)
find = data
data

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
data = data.dropna()
X = data.iloc[:, 0:-2]
X_norm = scaler.fit_transform(X)
#X_norm = scaler.transform(X)
y = data.iloc[:, -2]

x_train, x_test, y_train, y_test = train_test_split(X_norm, y, test_size = 0.2, random_state = 42)






dummy_recommended = ['Song1.mp3','Song2.mp3','Song3.mp3','Song4.mp3','Song5.mp3']
pygame.mixer.init() # initializing the mixer
    
def stop():
    pygame.mixer.music.stop()


def song_player():
    global m_screen, audio_file_name  
    if audio_file_name: # play sound if just not an empty string
        #noise = pygame.mixer.Sound(audio_file_name)
        
        print(audio_file_name)
        pygame.mixer.music.load(audio_file_name)
        pygame.mixer.music.play()


root = Tk()
root.geometry("600x650")

root.title("Music Recommendation System")

#root.configure(bg='white')

#label = Label(root, text ="Welcome to Musix  : Group 3", foreground = "teal", font = fontStyle,pady = 70).pack()
logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.pack()
labels = []
audio_file_name = ''

def clear():
    label1.pack_forget()
    label2.pack_forget()
    song1.pack_forget()
    song2.pack_forget()
    song3.pack_forget()
    song4.pack_forget()
    song5.pack_forget()
    play_button.pack_forget()
    stop_button.pack_forget()
    
    b1['state'] = NORMAL
    b2['state'] = DISABLED
    
def open_masker():
    c =0
    global audio_file_name
    fontStyle = tkFont.Font(family="Raleway")
    fontStyle2 = tkFont.Font(family="Courier", size=10)
    audio_file_name = filedialog.askopenfilename(filetypes=(("Audio Files", ".mp3"),   ("All Files", "*.*")))
    global label1,label2,song1,song2,song3,song4,song5,play_button,stop_button
    if audio_file_name: # play sound if just not an empty string
        b2['state'] = NORMAL
        c = 1
        filename = os.path.basename(audio_file_name)
        label1 = Label(root, text = "You have Selcted : "+filename, foreground = "teal",pady = 10,font = fontStyle)
        label1.pack()
        
        data1 = []
        list1 = []
        songData = []
        y, sr = librosa.load(audio_file_name, mono=True, duration=20)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        songData.append(tempo)
        songData.append(mean(beats))
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        songData.append(mean(chroma_stft.flatten()))
        # rmse = librosa.feature.rmse(y=y)
        rmse=librosa.feature.rms(y=y)[0]
        songData.append(mean(rmse))
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        songData.append(mean(spec_cent.flatten()))
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        songData.append(mean(spec_bw.flatten()))
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        songData.append(mean(rolloff.flatten()))
        zcr = librosa.feature.zero_crossing_rate(y)
        songData.append(mean(zcr.flatten()))
        # zcr1 = librosa.feature.zero_crossing_rate(y)
        # songData.append(mean(zcr1.flatten()))
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        for i in mfcc:
            songData.append(np.mean(i))
            list1.append(np.mean(i))

        data1.append(songData)
        
        model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
        model_knn.fit(x_train)
        
        query_index = data1
        distances, indices = model_knn.kneighbors(data1, n_neighbors = 23)
        
        knn = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), 
                  key=lambda x: x[1])[:0:-1]
        
        selected_knn_ind = []
        for i in range(0,5):
            selected_knn_ind.append(knn[i][0])
            
        selected_knn_file = []
        for i in selected_knn_ind:
            selected_knn_file.append(os.path.basename(find.iloc[i][29]))
            
        
    
        play_button = Button(root, text = 'Play',command = song_player,font = "Raleway", bg="#008080",fg="white",width=10)
        play_button.pack(anchor = CENTER)
        
        stop_button = Button(root, text = 'Stop',command = stop,font = "Raleway", bg="#008080",fg="white",width=10)
        stop_button.pack(anchor = CENTER,pady=10)
        
        label2 = Label(root, text = "Recommended Songs Are : ", foreground = "teal",font = fontStyle)
        label2.pack(pady=20)
        
        
        #for i in range(len(dummy_recommended)):
        song1 = Label(root, text = "Song 1: "+selected_knn_file[0], foreground = "teal",font = fontStyle)
        song1.pack(pady=3)
        song2 = Label(root, text = "Song 2: "+selected_knn_file[1], foreground = "teal",font = fontStyle)
        song2.pack(pady=3)
        song3 = Label(root, text = "Song 3: "+selected_knn_file[2], foreground = "teal",font = fontStyle)
        song3.pack(pady=3)
        song4 = Label(root, text = "Song 4: "+selected_knn_file[3], foreground = "teal",font = fontStyle)
        song4.pack(pady=3)
        song5 = Label(root, text = "Song 5: "+selected_knn_file[4], foreground = "teal",font = fontStyle)
        song5.pack(pady=3)
        
        
        
        b1['state'] = DISABLED
    

b1 = Button(root, text = 'Select Input',command = open_masker,font = "Raleway", bg="#008080",fg="white",height=1,width=10)

b1.pack(anchor = CENTER,pady=10)

b2 = Button(root, text = 'Clear Output',command = clear,font = "Raleway", bg="#008080",fg="white",height=1,width=10, state=DISABLED)
b2.pack(anchor = CENTER, pady=10)


root.mainloop()