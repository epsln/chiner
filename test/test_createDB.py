import unittest
import random
import os
import numpy as np
import shutil
import json 
import configparser

import createDB 


class testCreateDB(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.config = configparser.ConfigParser()
        self.config.read(r'configTest.cfg')
        self.dbName = self.config.get('Database', 'name') + ".json"

        createDB.debugFlag = True
        createDB.main()

    def test_fileExist(self):
        self.assertTrue(os.path.exists(self.dbName))

    def test_notEmpty(self):
        self.assertFalse(os.stat(self.dbName).st_size == 0)

    def test_canReadSongs(self):
        with open(self.dbName) as jsonFile:
            data = json.load(jsonFile)
        jsonFile.close()
        for song in data:
            self.assertTrue(os.path.exists(song['path']))

    @classmethod
    def tearDownClass(self):
        os.remove(self.dbName)

if __name__ == '__main__':
    unittest.main()

