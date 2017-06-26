import unittest
import pandas as pd
import random
from src.utilities.data_utils import *

TEST_PROGRAM_BOUNDARY_FILEPATH = 'test_data/'
TEST_CAPTION_FILEPATH = 'test_data/'

class TestDataUtil(unittest.TestCase):
    def setUp(self):
        self.test_caption_num = 5
        self.test_caption_filename = {'prefix': 'test_caption_', 'ext': '.txt3'}
        self.test_cut_num = 5
        self.test_cut_filename = {'prefix': 'test_program_cuts_', 'ext': '.cuts'}


    def test_load_single_caption_data(self):    
        i = random.randrange(self.test_caption_num)
        filename = ''.join([self.test_caption_filename['prefix'], str(i),
                            self.test_caption_filename['ext']])

        path = ''.join([TEST_PROGRAM_BOUNDARY_FILEPATH, filename])
        df, _, _ = load_caption_data(path)
        
        self.assertEqual(len(df.columns), 5, 'should have 5 columns')
        self.assertTrue(df.loc[0]['marker'].startswith('SEG'), 'should have marker column starting with SEG')


    # def test_load_batch_caption_data(self):
    #     self.assertEqual('failing', '', 'must batch multiple caption data')


    def test_load_single_cut_data(self):    
        i = random.randrange(self.test_cut_num)
        filename = ''.join([self.test_cut_filename['prefix'], str(i),
                            self.test_cut_filename['ext']])
        
        path = '{}{}'.format(TEST_PROGRAM_BOUNDARY_FILEPATH, filename)
        y = load_program_cut_data(path)

        self.assertEqual(len(y.columns), 3, 'should have 3 columns')
        self.assertIsInstance(y.loc[0]['cutpoint'], pd.Timestamp, 'should have marker column starting with SEG')


    # def test_load_batch_cut_data(self):    
    #     self.assertEqual('failing', '', 'must batch multiple caption data')

if __name__ == '__main__':
    unittest.main()
