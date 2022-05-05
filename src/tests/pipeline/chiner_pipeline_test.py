import unittest

from src.chiner.pipeline import ChinerPipeline


class TestChinerPipeline(unittest.TestCase):
    def test_init(self):
        pipe = ChinerPipeline()
