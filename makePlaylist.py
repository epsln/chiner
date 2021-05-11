import json
import numpy as np
import random
from scipy.spatial import distance
import configparser
import tinydb

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
        dbName = "test/" + config.get('Database', 'name')
    else:
        config.read(r'config.cfg')
        dbName = config.get('Database', 'name') + '.json'

    saveDir = config.get('Playlist', 'directory') 
    pName = config.get('Playlist', 'name')
    numTracks = int(config.get('Playlist', 'duration'))
    similarityFun = config.get('Playlist', 'similarityFun')
    pMode = config.get('chiner', 'PartyMode')

    if pMode == False:
        playlistFile = open(pName + ".m3u", "w+")
    if similarityFun == "L2":
        distFun = distance.euclidean
    if similarityFun == "cosine":
        distFun = spatial.distance.cosine

    dbSong = tinydb.TinyDB(dbName)
    
    currentTrack = random.choice(dbSong.all())
    alreadySeen = []
    for i in range(numTracks):
        currentTrack = findClosest(currentTrack, dbSong.all(), alreadySeen, distFun)
        alreadySeen.append(currentTrack)
        if pMode == False:
            playlistFile.write(currentTrack['path'] + "\n")
        #Empty already seen sometimes
    #Party mode : stay active and add a track if mpd playlist < length

if __name__ == "__main__":
    main()
