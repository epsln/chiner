import json
import numpy as np
import random

numTracks = 5

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


with open("test.json") as jsonFile:
    data = json.load(jsonFile)
jsonFile.close()

currentTrack = random.choice(data)
alreadySeen = []
with open("test.m3u") as playlistFile:
    for i in range(numTracks):
        currentTrack = findClosest(currentTrack, data, alreadySeen)
        alreadySeen.append(currentTrack)
        print(currentTrack['path'])


