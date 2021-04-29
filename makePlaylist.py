import json
import numpy as np
import random
from scipy.spatial import distance
import configparser

debugFlag = False 

def findClosest(currentTrack, data, alreadySeen, distFun):
    minDist = 10000000
    for track in data:
        if track['path'] == currentTrack['path']: #skip if is the same as current
            continue #Redo it via unique id or somethin
        
        currEmbed = np.array(currentTrack['embed']).flatten()
        testEmbed = np.array(track['embed']).flatten()
        dist = distFun(currEmbed, testEmbed)
        if dist < minDist and track not in alreadySeen:
            minDist = dist
            nextTrack = track
    return nextTrack 


def loadData(dbName):
    with open(dbName) as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    return data


def main():
    config = configparser.ConfigParser()
    if debugFlag == True:
        config.read(r'configTest.cfg')
    else:
        config.read(r'config.cfg')

    dbName = config.get('Database', 'name') + '.json'
    saveDir = config.get('Playlist', 'directory') 
    pName = config.get('Playlist', 'name')
    numTracks = int(config.get('Playlist', 'duration'))
    similarityFun = config.get('Playlist', 'similarityFun')
    if similarityFun == "L2":
        distFun = distance.euclidean
    if similarityFun == "cosine":
        distFun = spatial.distance.cosine

    data = loadData(dbName)
    currentTrack = random.choice(data)
    alreadySeen = []
    with open(pName + ".m3u", "w+") as playlistFile:
        for i in range(numTracks):
            currentTrack = findClosest(currentTrack, data, alreadySeen, distFun)
            alreadySeen.append(currentTrack)
            playlistFile.write(currentTrack['path'] + "\n")
            #Empty already seen sometimes

if __name__ == "__main__":
    main()
