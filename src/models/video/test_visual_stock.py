import unittest
import os
import warnings
warnings.filterwarnings("ignore")

from src.models.video.visualstock import VisualStock
from src import ROOT_DIR

DEJAVU_CONFIG_PATH = ROOT_DIR + '/models/audio/dejavu.cnf'
TEST_PATH = ROOT_DIR + '/../data/example/example.mp4'
TEST_SEG_PATH = ROOT_DIR + '/../data/example/audio_seg.mp3'

CUTFILE_PATH = ROOT_DIR + '/../data/example/example.cuts'

class TestFingerPrint(unittest.TestCase):    
    def setUp(self):
        self.vs = VisualStock()

    def test_extract_visual_stock(self):
        pass

    def test_slice_video_segment(self):
        pass


if __name__ == '__main__':
    unittest.main()
