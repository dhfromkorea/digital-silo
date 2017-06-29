import unittest
import numpy as np
import random
import glob
from src.models.text.keyword_search import *
from src.utilities.data_utils import *


class TestKeywordSearchModel(unittest.TestCase):
    
    def setUp(self):
        search_path = 'test_data/' + '*.txt3'
        file_paths = glob.glob(search_path)
        file_path = random.choice(file_paths)

        caption_data, metadata = next(load_caption_files(file_path))                        
        self.X = split_caption_to_docs(caption_data)
        self.X_metadata = metadata

        self.keywords = ['caption', 'story', 'commercial']
        self.model = KeywordSearch(self.keywords)


    def test_find_lines_match_single_keyword(self):
        self.model.keywords = self.keywords[0:1]
        
        matched_lines = self.model.predict(self.X)
        line = matched_lines['caption'].iloc[0].lower()
        self.assertTrue(self.keywords[0] in line,'keyword-matching lines must contain the searched-for keyword')


    def test_find_lines_match_multiple_keywords(self):
        self.model.keywords = self.keywords
        matched_lines = self.model.predict(self.X)
        line = matched_lines['caption'].iloc[0].lower()
        check_matches = any([w in line for w in self.keywords])
        self.assertTrue(check_matches,'keyword-matching lines must contain any of the keywords searched for')


    # def test_merge_neighboring_caption_lines(self):
    #     self.assertTrue(self.model.merge_time_window == 0, 'merge time window should be zero')
    #     MERGE_TIME_WINDOW = 5
    #     self.model.merge_time_window = MERGE_TIME_WINDOW 
    #     self.assertTrue(self.model.merge_time_window == 5, 'merge time window should be 5 minutes')

    #     matched_lines = self.model.predict(self.X)

    #     deltas = matched_lines['mid'].diff().dropna()
    #     is_merged = all(deltas > np.timedelta64(MERGE_TIME_WINDOW, 's'))
        
    #     msg = 'the lines that are off by less than {} seconds must be merged'
    #     self.assertTrue(is_merged, msg.format(MERGE_TIME_WINDOW))


if __name__ == '__main__':
    # TODO: is this the right thing todo ?
    unittest.main()
