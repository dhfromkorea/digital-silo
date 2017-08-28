import unittest
import os
import warnings
warnings.filterwarnings("ignore")

from src.models.audio.fingerprint import FingerPrint
from src import ROOT_DIR

DEJAVU_CONFIG_PATH = ROOT_DIR + '/models/audio/dejavu.cnf'
TEST_PATH = ROOT_DIR + '/../data/example/example.mp4'
TEST_SEG_PATH = ROOT_DIR + '/../data/example/audio_seg.mp3'

CUTFILE_PATH = ROOT_DIR + '/../data/example/example.cuts'

class TestFingerPrint(unittest.TestCase):    
    def setUp(self):
        self.fp = FingerPrint(DEJAVU_CONFIG_PATH)
        self.filepath = TEST_PATH 

    def test_slice_audio_segment(self):
        pb = 20000 # program boundary timestamp in secs
        pad = 10 # secs
        self.fp.slice_audio_segment(self.filepath, pb - pad, pb + pad, "mp4")
        import os.path
        self.assertTrue(os.path.isfile(self.filepath), "The sliced segment should have been saved.")

    def test_extract_fingerprint_single(self):
        self.fp.extract_fingerprint_single(TEST_SEG_PATH)
        # song once extracted must be recognized
        song = self.fp.recognize_audio(TEST_SEG_PATH)
        self.assertTrue(song['confidence'] > 5000, "fingerprint for a song the model has already seen must be recognized with high confidence.")


    def test_slice_with_cutfiles(self):
        # TODO: test with correct cutfiles
        pass 
        # self.fp.slice_with_cutfiles(CUTFILE_PATH)


    def test_extract_fingerprint_directory(self):
        # TODO: test only on seg files 
        pass
        # self.fp.extract_fingerprint_directory(self.filepath)
        # # song once extracted must be recognized
        # song = self.recognize_audio(self.filepath)
        # self.assertEqual(song, {}, "")


if __name__ == '__main__':
    unittest.main()
