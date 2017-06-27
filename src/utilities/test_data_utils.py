import unittest
import pandas as pd
import random
import glob
import os
from src.utilities.data_utils import *


TEST_DATA_PATH = 'test_data/'

class TestDataUtilCaption(unittest.TestCase):
    def setUp(self):
        self.root_path = TEST_DATA_PATH
        search_path = self.root_path + '*.txt3'
        self.file_paths = [p for p in glob.iglob(search_path)]


    def test_load_single_caption_file(self):
        file_path = random.choice(self.file_paths)
        files = load_caption_files(file_path)                
        df, metadata = next(files)

        self.assertEqual(len(df.columns), 5, 'should have 5 columns')
        self.assertTrue(df.loc[0]['marker'].startswith('SEG'), 'should have marker column starting with SEG')
    

    def test_extract_metadata_caption_file(self):
        file_path = random.choice(self.file_paths)
        files = load_caption_files(file_path)                
        _, metadata = next(files)

        filename = os.path.basename(file_path)
        filename_from_metadata = '{}{}'.format(metadata['filename'], metadata['filetype'])
        self.assertEqual(filename, filename_from_metadata, 'the filename that we loaded data from must match the filename extracted in the metadata.')


    def test_load_multiple_caption_files(self):
        # should look for *txt recursively in root
        files = load_caption_files(self.root_path, recursive_search=True)

        num_files = 0
        for f in files:
            df, _ = f
            num_files += 1
            self.assertEqual(len(df.columns), 5, 'should have 5 columns')
            self.assertTrue(df.loc[0]['marker'].startswith('SEG'), 'should have marker column starting with SEG')
        self.assertTrue(num_files > 1, 'it should load more than one caption file.')


class TestDataUtilProgramCut(unittest.TestCase):
    def setUp(self):
        self.root_path = TEST_DATA_PATH
        search_path = self.root_path + '*.cuts'
        self.file_paths = [p for p in glob.iglob(search_path)]


    def test_load_single_cut_file(self):    
        file_path = random.choice(self.file_paths)
        files = load_program_cut_files(file_path)                
        y, _ = next(files)

        self.assertEqual(len(y.columns), 3, 'should have 3 columns')
        self.assertIsInstance(y.loc[0]['cutpoint'], pd.Timestamp, 'should have marker column starting with SEG')


    def test_extract_metadata_cut_file(self):
        file_path = random.choice(self.file_paths)
        files = load_program_cut_files(file_path)
        _, metadata = next(files)

        filename = os.path.basename(file_path)
        filename_from_metadata = '{}{}'.format(metadata['filename'], metadata['filetype'])
        self.assertEqual(filename, filename_from_metadata, 'the filename that we loaded data from must match the filename extracted in the metadata.')


    def test_load_multiple_cut_files(self):
        files = load_program_cut_files(self.root_path, recursive_search=True)

        num_files = 0
        for f in files:
            y, metadata = f
            num_files += 1
            self.assertEqual(len(y.columns), 3, 'should have 3 columns')
            self.assertIsInstance(y.loc[0]['cutpoint'], pd.Timestamp, 'should have marker column starting with SEG')                    
        self.assertTrue(num_files > 1, 'it should load more than one cut file.')

if __name__ == '__main__':
    unittest.main()
