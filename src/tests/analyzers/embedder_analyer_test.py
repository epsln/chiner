import unittest
from unittest.mock import MagicMock 
import torch 

from src.chiner.analyzers import EmbedderAnalyzer


class TestImageAnalyzer(unittest.TestCase):
    def test_init(self):
        embedder = EmbedderAnalyzer(MagicMock(spec = torch.nn.Module), 128) 
