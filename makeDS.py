#Create a dataset of normalised spectrograms from files
import os
import numpy as np
import librosa
import audiofile as af

import configparser

from utils.audioTools import getSpectro

config = configparser.ConfigParser()
config.read(r'config.cfg')
dsName = config.get('Dataset', 'name')
fftLength = int(config.get('Dataset', 'fftLength'))
nFreq = int(config.get('Dataset', 'nFreq')) 
numFeatures = int(config.get('Dataset', 'numFeatures'))


#Might want to rename data to fit whatever user might want
musicFiles = [os.path.join(path, name) for path, subdirs, files in os.walk("data/") for name in files] 

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
         
    for i, song in enumerate(musicFiles):

            S = getSpectro(song, fftLength)
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
