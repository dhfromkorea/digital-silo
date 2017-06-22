import unittest
import pandas as pd
import random
from data_utils import *

TEST_PROGRAM_BOUNDARY_FILEPATH = 'test_data/'
TEST_CAPTION_FILEPATH = 'test_data/'

class TestDataUtil(unittest.TestCase):
    def setUp(self):
        self.test_caption_num = 5
        self.test_caption_filename = {'prefix': 'test_caption_', 'ext': '.txt3'}
        self.test_cut_num = 5
        self.test_cut_filename = {'prefix': 'test_cut', 'ext': '.cuts'}


    def test_load_single_caption_data(self):    
        i = random.randrange(self.test_caption_num)
        filename = ''.join([self.test_caption_filename['prefix'], str(i),
                            self.test_caption_filename['ext']])
        path = ''.join([TEST_PROGRAM_BOUNDARY_FILEPATH, filename])
        df, _, _ = load_caption_data(path)
        
        self.assertEqual(len(df.columns), 5, 'should have 5 columns')
        self.assertTrue(df.loc[0]['marker'].startswith('SEG'), 'should have marker column starting with SEG')


    def test_load_multiple_caption_data(self):
        self.assertEqual('df', '')


    def test_load_single_cut_data(self):    
        path = '{}{}'.format(TEST_PROGRAM_BOUNDARY_FILEPATH, 'test_caption.txt3')
        self.assertEqual('df', '')


    def test_load_multiple_cut_data(self):    
        self.assertEqual('df', '')

if __name__ == '__main__':
    unittest.main()
