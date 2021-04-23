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

searchDir = "data/"
M = 1024 

def root_mean_squared_error(y_true, y_pred):
            return K.sqrt(K.mean(K.square(y_pred - y_true))) 
        
def getSpectro(audioData):
    #We create a 3D tensor using 3 type of feature 
    #Mel spectrogram 

    
    audioData = librosa.util.normalize(audioData)
    stft = np.abs(librosa.core.stft(audioData)) ** 2 #Make spectro once so we don't have to recompute it


    #Mel spectrogram 
    melSpec = librosa.feature.melspectrogram(S = stft)
    mfcc    = librosa.feature.mfcc(S = stft)
    chroma  = librosa.feature.chroma_stft(S = stft)

    #Grab a random start idx to slice the array
    #TODO: Figure out a way to get a M length feature by cutting audioData directly
    idxSection = int(np.random.uniform(0, melSpec.shape[1] - M))

    melSpec = melSpec[:, idxSection:idxSection + M]
    mfcc    = mfcc[:, idxSection:idxSection + M]
    chroma  = chroma[:, idxSection:idxSection + M]

    melSpec = np.log(melSpec + 1e-9)
        
    melSpec = librosa.util.normalize(melSpec)
    mfcc    = librosa.util.normalize(mfcc)
    chroma  = librosa.util.normalize(chroma)

    #Pad to fit the shape of melSpec
    mfcc    = np.pad(mfcc, pad_width=((0, 108), (0, 0)))
    chroma  = np.pad(chroma, pad_width=((0, 116), (0, 0)))[:, :M]
    
    #add axis to concatenate
    chroma  = np.expand_dims(chroma, axis = 0)


    #Stack it up into a 3D Matrix
    S = np.stack((melSpec, mfcc))
    S = np.concatenate((S, chroma))
    S = np.swapaxes(S, 0, 2)
    S = np.expand_dims(S, axis=0)

    
    return S

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

    spectro = getSpectro(audioData)
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

