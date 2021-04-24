import unittest
import random
import os
import numpy as np

from utils import audioTools

#Get this from a config file
fftLength = 4096
nFreq = 128
numFeatures = 3
musicFiles = [os.path.join(path, name) for path, subdirs, files in os.walk("data/") for name in files] 

spectro = audioTools.getSpectro(random.choice(musicFiles), fftLength)

class testSpectro(unittest.TestCase):

    def test_shape(self):
        self.assertEqual(spectro.shape,(fftLength, nFreq, numFeatures))

    def test_type(self):
        self.assertEqual(spectro.dtype, 'float32')

    def test_validVal(self):
        #Check if there are invalid values by summing and checking if res is nan or inf
        self.assertFalse(np.isnan(np.sum(spectro)))
        self.assertFalse(np.isinf(np.sum(spectro)))

if __name__ == '__main__':
    unittest.main()

