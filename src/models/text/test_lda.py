import unittest
import numpy as np
import random
import glob
from src.models.text.lda import *
from src.utilities.data_utils import *


class TestLda(unittest.TestCase):
    
    def setUp(self):
        search_path = 'test_data/' + '*.txt3'
        file_paths = glob.glob(search_path)
        file_path = random.choice(file_paths)

        caption_data, metadata = next(load_caption_files(file_path))                        
        self.X = split_caption_to_X(caption_data)
        self.X_metadata = metadata




if __name__ == '__main__':
    # TODO: is this the right thing todo ?
    unittest.main()
