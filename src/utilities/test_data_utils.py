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


    def test_load_single_caption_file(self):    
        i = random.randrange(self.test_caption_num)
        filename = ''.join([self.test_caption_filename['prefix'], str(i),
                            self.test_caption_filename['ext']])

        single_file_path = ''.join([TEST_PROGRAM_BOUNDARY_FILEPATH, filename])
        files = load_caption_files(single_file_path)
        
        for f in files:
            df, metadata = f

        self.assertEqual(len(df.columns), 5, 'should have 5 columns')
        self.assertTrue(df.loc[0]['marker'].startswith('SEG'), 'should have marker column starting with SEG')


    def test_load_multiple_caption_files(self):
        # should look for *txt recursively in root
        path = 'test_data/'
        files = load_caption_files(path, recursive_search=True)

        num_files = 0
        for f in files:
            df, metadata = f
            num_files += 1
            self.assertEqual(len(df.columns), 5, 'should have 5 columns')
            self.assertTrue(df.loc[0]['marker'].startswith('SEG'), 'should have marker column starting with SEG')
        self.assertTrue(num_files > 1, 'it should load more than one caption file.')


    def test_load_single_cut_file(self):    
        i = random.randrange(self.test_cut_num)
        filename = ''.join([self.test_cut_filename['prefix'], str(i),
                            self.test_cut_filename['ext']])
        
        path = '{}{}'.format(TEST_PROGRAM_BOUNDARY_FILEPATH, filename)
        y = load_program_cut_files(path)

        self.assertEqual(len(y.columns), 3, 'should have 3 columns')
        self.assertIsInstance(y.loc[0]['cutpoint'], pd.Timestamp, 'should have marker column starting with SEG')


    def test_load_multiple_cut_files(self):
        
        self.assertEqual('failing', '', 'must batch multiple caption data')

if __name__ == '__main__':
    unittest.main()
