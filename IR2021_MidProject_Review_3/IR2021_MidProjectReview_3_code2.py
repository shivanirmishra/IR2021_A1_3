
import os
import sys
import time
import glob
import datetime
import sqlite3
import numpy as np 
msd_subset_path='C:\\Users\\Akanksha\\Downloads\\millionsongsubset'
msd_subset_data_path=os.path.join(msd_subset_path,'MillionSongSubset')
msd_subset_addf_path=os.path.join(msd_subset_path,'AdditionalFiles')
assert os.path.isdir(msd_subset_path),'wrong path' 
assert os.path.isdir(msd_subset_addf_path),'wrong path'
msd_code_path='C:\\Users\\Akanksha\\Downloads\\MSongsDB'
assert os.path.isdir(msd_code_path),'wrong path'

import hdf5_getters as GETTERS


def strtimedelta(starttime,stoptime):
    return str(datetime.timedelta(seconds=stoptime-starttime))


def apply_to_all_files(basedir,func=lambda x: x,ext='.h5'):
    

    cnt = 0

    for root, dirs,files in os.walk(basedir):

        files = glob.glob(os.path.join(root,'*'+ext))

        cnt += len(files)

        for f in files :
            func(f) 
        
    return cnt

print('number of song files:',apply_to_all_files(msd_subset_data_path))


all_artist_names = []

def func_to_get_artist_name(filename):

    h5 = GETTERS.open_h5_file_read(filename)
    artist_name = GETTERS.get_artist_name(h5)
    all_artist_names.append( artist_name )
    h5.close()
    
all_artist_ids = []

def func_to_get_artist_ids(filename):

    h5 = GETTERS.open_h5_file_read(filename)
    artist_ids = GETTERS.get_artist_id(h5)
    all_artist_ids.append( artist_ids )
    h5.close()
all_similar_artists = []


def func_to_get_similar_artists(filename):

    h5 = GETTERS.open_h5_file_read(filename)
    artist_similar = GETTERS.get_similar_artists(h5)
    all_similar_artists.append( artist_similar )
    h5.close()
    
all_artist_hotness = []


def func_to_get_artist_hotness(filename):

    h5 = GETTERS.open_h5_file_read(filename)
    artist_hotness = GETTERS.get_artist_hotttnesss(h5)
    all_artist_hotness.append( artist_hotness )
    h5.close()

all_song_hotness = []

def func_to_get_song_hotness(filename):

    h5 = GETTERS.open_h5_file_read(filename)
    song_hotness = GETTERS.get_song_hotttnesss(h5)
    all_song_hotness.append( song_hotness )
    h5.close()
    
all_energy = []


def func_to_get_energy(filename):

    h5 = GETTERS.open_h5_file_read(filename)
    energy = GETTERS.get_energy(h5)
    all_energy.append( energy )
    h5.close()

    
all_loudness = []
def func_to_get_loudness(filename):

    h5 = GETTERS.open_h5_file_read(filename)
    loudness = GETTERS.get_loudness(h5)
    all_loudness.append( loudness )
    h5.close()

all_mode = []

def func_to_get_mode(filename):

    h5 = GETTERS.open_h5_file_read(filename)
    mode = GETTERS.get_mode(h5)
    all_mode.append( mode )
    h5.close()

all_tempo = []

def func_to_get_tempo(filename):

    h5 = GETTERS.open_h5_file_read(filename)
    tempo = GETTERS.get_tempo(h5)
    all_tempo.append( tempo )
    h5.close()

all_track_id = []


def func_to_get_track_id(filename):

    h5 = GETTERS.open_h5_file_read(filename)
    track_id = GETTERS.get_track_id(h5)
    all_track_id.append( track_id )
    h5.close()

all_year = []

def func_to_get_year(filename):

    h5 = GETTERS.open_h5_file_read(filename)
    year = GETTERS.get_year(h5)
    all_year.append( year )
    h5.close()

apply_to_all_files(msd_subset_data_path,func=func_to_get_artist_name)
t2 = time.time()


apply_to_all_files(msd_subset_data_path,func=func_to_get_artist_ids)
t2 = time.time()

apply_to_all_files(msd_subset_data_path,func=func_to_get_similar_artists)
t2 = time.time()

apply_to_all_files(msd_subset_data_path,func=func_to_get_artist_hotness)
t2 = time.time()

apply_to_all_files(msd_subset_data_path,func=func_to_get_song_hotness)
t2 = time.time()

apply_to_all_files(msd_subset_data_path,func=func_to_get_energy)
t2 = time.time()

apply_to_all_files(msd_subset_data_path,func=func_to_get_loudness)
t2 = time.time()

apply_to_all_files(msd_subset_data_path,func=func_to_get_mode)
t2 = time.time()

apply_to_all_files(msd_subset_data_path,func=func_to_get_tempo)
t2 = time.time()

apply_to_all_files(msd_subset_data_path,func=func_to_get_track_id)
t2 = time.time()

apply_to_all_files(msd_subset_data_path,func=func_to_get_year)
t2 = time.time()

import pandas as pd
df = pd.DataFrame(list(zip(all_artist_ids,all_artist_names,all_similar_artists,all_artist_hotness,all_song_hotness,all_energy,all_loudness,all_mode,all_tempo,all_track_id,all_year )),columns = ['Artist Id','Artist Names','Similar Artists','Artist Hotness','Song Hotness','Energy','Loudness','Mode','Tempo','Track_id','Year'])
print(df)

df.to_csv('Dataset.csv', sep='\t', index=False,header=True) 


