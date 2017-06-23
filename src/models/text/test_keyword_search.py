import unittest
import numpy as np
from keyword_search import *
from utilities.data_utils import load_caption_data

class TestKeywordSearchModel(unittest.TestCase):
    def setUp(self):
        df, _, _ = load_caption_data()
        self.caption_data = df
        self.model = KeywordSearch()
        self.keywords = ['caption', 'story', 'commercial']
        #TODO: have a db of commonly used words

    def test_find_lines_match_single_keyword(self):
        keywords = self.keywords[0:1]
        matched_lines = self.model.predict(self.caption_data, keywords)
        lines = self.caption_data[matched_lines]
        line = lines['caption'].iloc[0].lower()
        check_match = any([w in line for w in keywords])
    
        self.assertTrue(check_match,'keyword-matching lines must contain the searched-for keyword')

    def test_find_lines_match_multiple_keywords(self):
        keywords = self.keywords
        matched_lines = self.model.predict(self.caption_data, keywords)
        lines = self.caption_data[matched_lines]
        
        line = lines['caption'].iloc[0].lower()
        check_matches = any([w in line for w in keywords])
        self.assertTrue(check_matches,'keyword-matching lines must contain any of the keywords searched for')

    def test_merge_neighboring_caption_lines(self):
        MIN_MERGE_DELTA = 5

        matched_lines = self.model.predict(self.caption_data, self.keywords, MIN_MERGE_DELTA)

        lines = self.caption_data[matched_lines]
        deltas = lines['mid'].diff()
        is_merged = all(deltas > np.timedelta64(MIN_MERGE_DELTA, 's'))
        
        self.assertTrue(is_merged, 'the lines that are off by less than and equal to {} seconds must be merged'.format(MIN_MERGE_DELTA))

if __name__ == '__main__':
    # TODO: is this the right thing todo ?
    unittest.main()
