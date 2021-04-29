import unittest
import random
import os
import numpy as np
import shutil

import configparser
import makePlaylist
import createDB 


class testPlaylist(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.config = configparser.ConfigParser()
        self.config.read(r'configTest.cfg')
        self.playlistName = self.config.get('Playlist', 'name') + ".m3u"
        self.numSongs = int(self.config.get('Playlist', 'duration'))

        makePlaylist.debugFlag = True
        makePlaylist.main()


    def test_fileExist(self):
        self.assertTrue(os.path.exists(self.playlistName))

    def test_notEmpty(self):
        self.assertFalse(os.stat(self.playlistName).st_size == 0)

    def test_canReadSongs(self):
        playlistFile = open(self.playlistName, 'r')
        lines = playlistFile.readlines()
        for line in lines:
            self.assertTrue(os.path.exists(line.replace('\n', '')))
        playlistFile.close()

    def test_numSong(self):
        #Check if we have the correct number of songs 
        #TODO: Change me once we go to duration in time of playlist
        numLines = sum(1 for line in open(self.playlistName))
        self.assertEqual(numLines, self.numSongs)

#    @classmethod
#    def tearDownClass(self):
#        os.rm(self.dbName)
#        os.rm(self.playlistName)

if __name__ == '__main__':
    unittest.main()

