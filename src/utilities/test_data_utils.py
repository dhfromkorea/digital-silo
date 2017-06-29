import unittest
import pandas as pd
import random
import glob
import os
import math
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
        X, metadata = next(files)

        self.assertEqual(len(X.columns), 5, 'should have 5 columns')
        self.assertTrue(X.loc[0]['marker'].startswith('SEG'), 'should have marker column starting with SEG')
    

    def test_load_multiple_caption_files(self):
        # should look for *txt recursively in root
        files = load_caption_files(self.root_path, recursive_search=True)

        num_files = 0
        for f in files:
            X, _ = f
            num_files += 1
            self.assertEqual(len(X.columns), 5, 'should have 5 columns')
            self.assertTrue(X.loc[0]['marker'].startswith('SEG'), 'should have marker column starting with SEG')

        self.assertTrue(num_files > 1, 'it should load more than one caption file.')


    def test_extract_metadata_caption_file(self):
        file_path = random.choice(self.file_paths)
        files = load_caption_files(file_path)                
        _, metadata = next(files)

        filename = os.path.basename(file_path)
        filename_from_metadata = '{}{}'.format(metadata['filename'], metadata['filetype'])
        self.assertEqual(filename, filename_from_metadata, 'the filename that we loaded data from must match the filename extracted in the metadata.')


    def test_split_caption_file_to_documents(self):
        file_path = random.choice(self.file_paths)
        files = load_caption_files(file_path)                
        X, metadata = next(files)
        docs = split_caption_to_docs(X, interval=10)
        
        #manually calculate the group size
        start_time = X.head(1).iloc[0]['start']
        # using 'start' is probably fine
        end_time = X.tail(1).iloc[0]['start']
        video_duration = end_time - start_time
        doc_size = np.timedelta64(10, 's')
        num_docs = math.ceil(video_duration / doc_size)
        
        self.assertEqual(len(docs), num_docs, 'a caption file should be split to a list of documents.')       


class TestDataUtilProgramCut(unittest.TestCase):
    def setUp(self):
        self.root_path = TEST_DATA_PATH
        search_path_y = self.root_path + '*.cuts'
        self.file_paths_y = [p for p in glob.iglob(search_path_y)]
        search_path_X = self.root_path + '*.txt3'
        self.file_paths_X = [p for p in glob.iglob(search_path_X)]


    def test_load_single_cut_file(self):    
        file_path = random.choice(self.file_paths_y)
        files = load_program_cut_files(file_path)                
        y, _ = next(files)

        self.assertEqual(len(y.columns), 3, 'should have 3 columns')
        self.assertIsInstance(y.loc[0]['cutpoint'], pd.Timestamp, 'should have marker column starting with SEG')


    def test_extract_metadata_cut_file(self):
        file_path = random.choice(self.file_paths_y)
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


    def test_convert_program_cuts_to_y(self):
        file_path = random.choice(self.file_paths_X)
        files = load_caption_files(file_path)                
        X, metadata = next(files)
        docs = split_caption_to_docs(X, interval=10)

        file_path = random.choice(self.file_paths_y)
        files = load_program_cut_files(file_path)                
        cuts, _ = next(files)

        y = convert_program_cuts_to_y(cuts, docs)
        self.assertEqual(len(y), len(docs), 'the lengths of docs and y should be the same.')
        
if __name__ == '__main__':
    unittest.main()
