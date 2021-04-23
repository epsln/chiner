#Create a dataset of normalised spectrograms from files
import os
import numpy as np
import librosa
import audiofile as af

from audioTools import getSpectro

dsName = "ds"

#Might want to rename data to fit whatever user might want
musicFiles = [os.path.join(path, name) for path, subdirs, files in os.walk("data/") for name in files] 
M = 4096# Num of timestep used for training

def main():

    #If folder already exist, quit
    if os.path.exists(dsName):
        print("ERROR:  The folder '" + dsName + "' already exists ! either delete it or rename it and try again")
#        return -1
    else:
        #Else create folder 
        os.makedirs(dsName)
        os.makedirs(dsName + "/train")
        os.makedirs(dsName + "/test/")
         

    #Might want to move this to its own file (the spectro and input creation)
    for i, song in enumerate(musicFiles):
#            audioData, sr = af.read(song) 
#            audioData = audioData[0, :]#Get mono
            #We create a 3D tensor using 3 type of feature: melspec, mfcc, chromaspec
            #mfcc and chroma dont have the same width, so we pad it to put it into a 3D tensor
            #We log scale and normalize everything
            #We use a random section of the track to have the best chance to capture the info
            
            #audioData, sr = librosa.load(song) 
            #audioData = librosa.util.normalize(audioData)
            #stft = np.abs(librosa.core.stft(audioData)) ** 2 #Make spectro once so we don't have to recompute it


            ##Mel spectrogram 
            #melSpec = librosa.feature.melspectrogram(S = stft)
            #mfcc    = librosa.feature.mfcc(S = stft)
            #chroma  = librosa.feature.chroma_stft(S = stft)

            ##Grab a random start idx to slice the array
            ##TODO: Figure out a way to get a M length feature by cutting audioData directly
            #idxSection = int(np.random.uniform(0, melSpec.shape[1] - M))

            #melSpec = melSpec[:, idxSection:idxSection + M]
            #mfcc    = mfcc[:, idxSection:idxSection + M]
            #chroma  = chroma[:, idxSection:idxSection + M]

            #melSpec = np.log(melSpec + 1e-9)
            #    
            #melSpec = librosa.util.normalize(melSpec)
            #mfcc    = librosa.util.normalize(mfcc)
            #chroma  = librosa.util.normalize(chroma)

            ##Pad to fit the shape of melSpec
            #mfcc    = np.pad(mfcc, pad_width=((0, 108), (0, 0)))
            #chroma  = np.pad(chroma, pad_width=((0, 116), (0, 0)))[:, :M]
            #
            ##add axis to concatenate
            #chroma  = np.expand_dims(chroma, axis = 0)

            ##Stack it up into a 3D Matrix
            #S = np.stack((melSpec, mfcc))
            #S = np.concatenate((S, chroma))
            #S = np.swapaxes(S, 0, 2)
            S = getSpectro(song, M)
            #And save
            if np.random.uniform(0, 1) > 0.8:
                print("Saving " + dsName + "/test/"+os.path.basename(song)[:-4]+".npy")
                print("[",i + 1,"/",len(musicFiles), "]")
                np.save(dsName + "/test/"+os.path.basename(song)[:-4]+".npy", S)
            else:
                print("Saving " + dsName + "/train/"+os.path.basename(song)[:-4]+".npy")
                print("[",i + 1,"/",len(musicFiles), "]")
                np.save(dsName + "/train/"+os.path.basename(song)[:-4]+".npy", S)

if __name__ == "__main__":
    main()
