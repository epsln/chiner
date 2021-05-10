import unittest
import random
import os
import shutil
import json 
import configparser
import tinydb

import createDB 


class testCreateDB(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.config = configparser.ConfigParser()
        self.config.read(r'configTest.cfg')
        self.dbName = self.config.get('Database', 'name')
        self.dbDir = self.config.get('Database', 'directory')
        self.dbName = os.path.join(self.dbDir, self.dbName)
        self.db = tinydb.TinyDB(self.dbName)

        createDB.debugFlag = True
        createDB.main()

    def test_fileExist(self):
        self.assertTrue(os.path.exists(self.dbName))

    def test_notEmpty(self):
        self.assertFalse(os.stat(self.dbName).st_size == 0)

    def test_canReadSongs(self):
        for song in self.db.all():
            self.assertTrue(os.path.exists(song['path']))

if __name__ == '__main__':
    unittest.main()

