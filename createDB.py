from tensorflow import keras

import os
import numpy as np
import librosa
from skimage import util
import sys
import json 
from tinydb import TinyDB, Query
import configparser

from utils.audioTools import getSpectro

debugFlag = False 

def root_mean_squared_error(y_true, y_pred):
            return K.sqrt(K.mean(K.square(y_pred - y_true))) 
        
def getDanceability(times, bpm):
    #Get the danceability of a song out of the onset strength of the beat
    #https://www.researchgate.net/publication/324672216_Score_Formulation_and_Parametric_Synthesis_of_Musical_Track_as_a_Platform_for_Big_Data_in_Hit_Prediction
    danceability = 0
    for val in times:
        if val > 1.0: #Might need to use derivatives to detect peaks, but thresholding might work fine
            danceability += bpm * val 
    return danceability 

def songAlreadyExist(songPath, songDB):
    songQuery = Query()
    a = songDB.search(songQuery.path == songPath)
    if songDB.search(songQuery.path == songPath):
        return True
    else:
        return False

def main():
    config = configparser.ConfigParser()
    if debugFlag == True:
        config.read(r'configTest.cfg')
    else:
        config.read(r'config.cfg')

    #TODO: If modelName is empty, grab the latest (highest ts)
    modelName = config.get('Model', 'name')
    fftLength = int(config.get('Dataset', 'fftLength'))
    nFreq = int(config.get('Dataset', 'nFreq')) 
    numFeatures = int(config.get('Dataset', 'numFeatures'))
    dbName = config.get('Database', 'name') + ".json"
    searchDir = config.get('Database', 'searchDir') 
    saveDir = config.get('Database', 'directory') 

    model = keras.models.load_model('models/' + modelName, custom_objects={'root_mean_squared_error': root_mean_squared_error})

    musicFiles = [os.path.join(path, name) for path, subdirs, files in os.walk(searchDir) for name in files] 
	
    songDB = TinyDB(os.path.join(saveDir, dbName))	
    jsonFile = open(saveDir + dbName + '.json', 'w+')
    #TODO: Add option to restart from stop point if catch interupt
    for i, song in enumerate(musicFiles):
        if i > 3 and debugFlag == True:
            break
        print("Analyzing " +os.path.basename(song))
        if songAlreadyExist(os.path.abspath(song), songDB) == True:
            print(song + " already exist in db, skipping")
            continue

        audioData, sr = librosa.load(song, sr=None) 

        spectro = getSpectro(song, fftLength, audioData)
        spectro = np.expand_dims(spectro, axis = 0)
        embed = model.predict(spectro)
        embed = embed.flatten()
        onset_env = librosa.onset.onset_strength(audioData, sr)
        bpm = librosa.beat.tempo(onset_envelope = onset_env, sr = sr)[0]
        times = librosa.times_like(onset_env, sr=sr)
        danceability = getDanceability(times, bpm) 

        songDB.insert({"path": os.path.abspath(song),
                "bpm": bpm,
                "danceability": danceability,
               "embed": embed.tolist()})
        print("[",i + 1,"/",len(musicFiles), "]")

if __name__ == "__main__":
    main()
