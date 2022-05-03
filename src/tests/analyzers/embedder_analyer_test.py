import numpy as np
import unittest
from unittest.mock import MagicMock 
import torch 

from src.chiner.analyzers import EmbedderAnalyzer


class TestEmbedderAnalyzer(unittest.TestCase):
    def test_init(self):
        embedder = EmbedderAnalyzer(MagicMock(spec = torch.nn.Module), 128) 

    def test_init_from_config(self):
        config = {"embedder":{
            "fft_length": 128,
            "path": "./model_simple.pth"
            }
        }
        embedder = EmbedderAnalyzer.from_config(config)

    def test_preprocess(self):
        embedder = EmbedderAnalyzer(model = MagicMock(spec = torch.nn.Module), fft_length = 128) 
        audio_data = np.random.random((128, 128))
        S = embedder._preprocess(audio_data)
        self.assertEqual(S.shape, (21, 1))


    def test_analyze(self):
        embedder = EmbedderAnalyzer(model = MagicMock(spec = torch.nn.Module), fft_length = 128) 
        input_data = np.random.uniform(size = (128, 1))
        embed = embedder._analyze(input_data)

    def test_postprocess(self):
        embedder = EmbedderAnalyzer(MagicMock(spec = torch.nn.Module), 128) 
        embedding = np.random.uniform((128, 1))
        encoded = embedder._postprocess(embedding)

