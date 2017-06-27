import unittest
import numpy as np
from src.models.text.keyword_search import *
from src.utilities.data_utils import load_caption_files

TEST_DB_PATH = 'test_data/'
TEST_CAPTION_FILE_PATH = TEST_DB_PATH + 'test_caption_0.txt3'

class TestKeywordSearchModel(unittest.TestCase):
    
    def setUp(self):
        files = load_caption_files(TEST_CAPTION_FILE_PATH)
        df, metadata = next(files)
        self.caption_data = df
        self.model = KeywordSearch()
        self.keywords = ['caption', 'story', 'commercial']
        #TODO: have a db of commonly used words

    def test_find_lines_match_single_keyword(self):
        keywords = self.keywords[0:1]
        matched_lines = self.model.predict(self.caption_data, keywords)
        line = matched_lines['caption'].iloc[0].lower()
        check_match = any([w in line for w in keywords])
    
        self.assertTrue(check_match,'keyword-matching lines must contain the searched-for keyword')

    def test_find_lines_match_multiple_keywords(self):
        keywords = self.keywords
        matched_lines = self.model.predict(self.caption_data, keywords)
        line = matched_lines['caption'].iloc[0].lower()
        check_matches = any([w in line for w in keywords])
        self.assertTrue(check_matches,'keyword-matching lines must contain any of the keywords searched for')

    def test_merge_neighboring_caption_lines(self):
        MERGE_TIME_WINDOW = 5 # minutes
        matched_lines = self.model.predict(self.caption_data, self.keywords, MERGE_TIME_WINDOW)

        deltas = matched_lines['mid'].diff().dropna()
        is_merged = all(deltas > np.timedelta64(MERGE_TIME_WINDOW, 's'))
        
        msg = 'the lines that are off by less than {} seconds must be merged'
        self.assertTrue(is_merged, msg.format(MERGE_TIME_WINDOW))


if __name__ == '__main__':
    # TODO: is this the right thing todo ?
    unittest.main()
