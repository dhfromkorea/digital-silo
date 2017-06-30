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
        self.X_paths = glob.glob(search_path)


    def test_load_single_caption_file(self):
        file_path = random.choice(self.X_paths)
        captions = load_caption_files(file_path)                
        caption, metadata = next(captions)

        cols = caption.columns.values
        self.assertTrue(all(cols == ['t_start', 'caption']), 'should have t_start and caption columns')
    

    def test_load_multiple_caption_files(self):
        # should look for *txt recursively in root
        captions = load_caption_files(self.root_path, recursive_search=True)
        n_captions = 0 
        for c in captions:
            n_captions += 1
        search_path_X = self.root_path + '*.txt3'
        paths = glob.glob(search_path_X)

        self.assertEqual(n_captions, len(paths), 'should load all caption files.')


    def test_extract_metadata_caption_file(self):
        file_path = random.choice(self.X_paths)
        captions = load_caption_files(file_path)                
        _, metadata = next(captions)

        filename = os.path.basename(file_path)
        filename_from_metadata = '{}{}'.format(metadata['filename'], metadata['filetype'])
        self.assertEqual(filename, filename_from_metadata, 'the filename that we loaded data from must match the filename extracted in the metadata.')


    def test_split_caption_file_to_X(self):
        file_path = random.choice(self.X_paths)
        captions = load_caption_files(file_path)                
        caption, metadata = next(captions)
        X = split_caption_to_X(caption, interval=10)
        num_X = X.shape[0]

        #manually calculate the group size
        start_time = X.head(1).iloc[0]['t_start']
        end_time = X.tail(1).iloc[0]['t_start']
        video_duration = end_time - start_time
        doc_size = np.timedelta64(10, 's')        
        num_segments = (video_duration // doc_size) + 1
        # off by one error does not matter
        self.assertTrue(num_X == num_segments, 'a caption file should be split to a list of documents.')     


class TestDataUtilProgramBoundary(unittest.TestCase):
    def setUp(self):
        self.root_path = TEST_DATA_PATH
        search_path_X = self.root_path + '*.txt3'
        self.X_paths = glob.glob(search_path_X)
        search_path_y = self.root_path + '*.cuts'
        self.y_paths = glob.glob(search_path_y)


    def test_load_single_program_boundary_file(self):    
        file_path = random.choice(self.y_paths)
        files = load_program_boundary_files(file_path)                
        p_boundaries, _ = next(files)

        cols = p_boundaries.columns.values
        self.assertTrue(all(cols == ['t_program_boundary']), 'should have t_start and caption columns')

    def test_load_multiple_program_boundary_files(self):
        p_boundary_files = load_program_boundary_files(self.root_path, recursive_search=True)

        num_p_boundary_files = 0
        for _ in p_boundary_files:
            num_p_boundary_files += 1
        
        search_path_y = self.root_path + '*.cuts'
        paths = glob.glob(search_path_y)

        self.assertEqual(num_p_boundary_files, len(paths), 'should load all program boundary files.')


    def test_extract_metadata_program_boundary_file(self):
        file_path = random.choice(self.y_paths)
        files = load_program_boundary_files(file_path)
        _, metadata = next(files)

        filename = os.path.basename(file_path)
        filename_from_metadata = '{}{}'.format(metadata['filename'], metadata['filetype'])
        self.assertEqual(filename, filename_from_metadata, 'the filename that we loaded data from must match the filename extracted in the metadata.')


    def test_convert_program_boundaries_to_y(self):
        file_path = random.choice(self.X_paths)
        files = load_caption_files(file_path)                
        caption, metadata = next(files)
        X = split_caption_to_X(caption, interval=10)

        file_path = random.choice(self.y_paths)
        files = load_program_boundary_files(file_path)                
        p_boundaries, _ = next(files)

        y = convert_program_boundaries_to_y(p_boundaries, X)
        self.assertEqual(len(y), len(X), 'the lengths of X and y should be the same.')
        
if __name__ == '__main__':
    unittest.main()
