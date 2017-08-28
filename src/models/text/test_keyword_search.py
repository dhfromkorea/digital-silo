import unittest
import numpy as np
import random
import glob
from src.models.text.keyword_search import *
from src.utilities.data_utils import *


class TestKeywordSearch(unittest.TestCase):
    
    def setUp(self):
        search_path = 'test_data/' + '*.txt3'
        file_paths = glob.glob(search_path)
        file_path = random.choice(file_paths)

        caption_data, metadata = next(load_caption_files(file_path))                        
        self.X = split_caption_to_X(caption_data)
        self.X_metadata = metadata

        self.keywords = ['caption', 'story', 'commercial']
        self.model = KeywordSearch(self.keywords)


    def test_find_lines_match_single_keyword(self):
        self.model.keywords = self.keywords[0:1]        
        is_matched = self.model.predict(self.X)
        matched_lines = self.X[is_matched]
        line = matched_lines['caption'].iloc[0].lower()
        import pdb;pdb.set_trace()
        self.assertTrue(self.keywords[0] in line,'keyword-matching lines must contain the searched-for keyword')


    def test_find_lines_match_multiple_keywords(self):
        self.model.keywords = self.keywords
        is_matched = self.model.predict(self.X)
        matched_lines = self.X[is_matched]

        line = matched_lines['caption'].iloc[0].lower()
        check_matches = any([w in line for w in self.keywords])
        self.assertTrue(check_matches,'keyword-matching lines must contain any of the keywords searched for')


if __name__ == '__main__':
    # TODO: is this the right thing todo ?
    unittest.main()
