from tensorflow import keras

import os
import pydub
import audiofile as af
import numpy as np
import librosa
from skimage import util
import sys
from PIL import Image
import json 

from utils.audioTools import getSpectro

searchDir = "data/"
M = 1024 

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


model = keras.models.load_model('models/test', custom_objects={'root_mean_squared_error': root_mean_squared_error})
model.summary()

musicFiles = [os.path.join(path, name) for path, subdirs, files in os.walk(searchDir) for name in files] 

outArr = []

jsonFile = open('test.json', 'w+')
for i, song in enumerate(musicFiles):
    print("Analyzing " +os.path.basename(song))
    #if os.stat("test.json").st_size > 0 and song in next((songAnalyzed for songAnalyzed in jsonFile if songAnalyzed["path"] == song), None) is not None:
    #     #If the song has already been analyzed, don't do it again
    #    continue

    audioData, sr = af.read(song) 
    audioData = audioData[0, :]#Get mono

    spectro = getSpectro(song, M)
    embed = model.predict(spectro)
    embed = embed.flatten()
    print(spectro[0, :, :, 0].shape)
    a = spectro[0, :, :, 0] * 255
    img = Image.fromarray(a)
    img = img.convert("L")
    img.save("spec.png")
    a = np.reshape(embed, (M, 128, 3))
    img = Image.fromarray(a[:,:,0] * 255)
    img = img.convert("L")
    img.save("embed.png")
    break
    onset_env = librosa.onset.onset_strength(audioData, sr)
    bpm = librosa.beat.tempo(onset_envelope = onset_env, sr = sr)[0]
    times = librosa.times_like(onset_env, sr=sr)
    danceability = getDanceability(times, bpm) 

    row = {"path": searchDir + song,
            "bpm": bpm,
            "danceability": danceability,
           "embed": embed.tolist()}
    outArr.append(row)
    print("[",i + 1,"/",len(musicFiles), "]")

json.dump(outArr, jsonFile)

