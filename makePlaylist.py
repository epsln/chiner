import json
import numpy as np
import random

import configparser

debugFlag = False 

def findClosest(currentTrack, data, alreadySeen):
    minDist = 10000000000
    for track in data:
        if track['path'] == currentTrack['path']: #skip if is the same as current
            continue #Redo it via unique id or somethin
        
        currEmbed = np.array(currentTrack['embed']).flatten()
        testEmbed = np.array(track['embed']).flatten()
        dist = np.linalg.norm(currEmbed- testEmbed) 
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

    data = loadData(dbName)
    currentTrack = random.choice(data)
    alreadySeen = []
    with open(pName + ".m3u", "w+") as playlistFile:
        for i in range(numTracks):
            currentTrack = findClosest(currentTrack, data, alreadySeen)
            alreadySeen.append(currentTrack)
            playlistFile.write(currentTrack['path'] + "\n")

if __name__ == "__main__":
    main()
